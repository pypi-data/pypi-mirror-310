import base64
import io
import tempfile
import uuid
from time import perf_counter
from typing import Generator
from unittest.mock import patch

import numpy as np
import pytest
from PIL import Image, ImageChops

from .embedding_models import EmbeddingModel
from .memory_types import LabeledMemory
from .repository import MemorysetConfig, MemorysetRepository
from .repository_lancedb import MemorysetLanceDBRepository
from .repository_milvus import MemorysetMilvusRepository
from .util import MemoryToInsert

MEMORYSET_METADATA = MemorysetConfig(
    embedding_dim=EmbeddingModel.CLIP_BASE.embedding_dim,
    embedding_model_name=EmbeddingModel.CLIP_BASE.name,
    embedding_model_max_seq_length_overwrite=None,
)


TEXT_DATA: list[MemoryToInsert] = [
    MemoryToInsert(
        text=text,
        label=label,
        label_name="positive" if label == 0 else "negative",
        metadata="{}",
        embedding=EmbeddingModel.CLIP_BASE.embed(text).tolist()[0],
        image=None,
        memory_id=str(uuid.uuid4()),
        memory_version=1,
    )
    for text, label in [
        ("I'm over the moon with how things turned out!", 0),
        ("This is the happiest I've felt in a long time.", 0),
        ("My heart feels so full and content.", 0),
        ("Everything feels perfect right now, I couldn't ask for more.", 0),
        ("I am so fed up with dealing with this over and over.", 1),
        ("Why does it always feel like I'm hitting a brick wall?", 1),
        ("I'm getting really tired of this never-ending cycle.", 1),
        ("It's so frustrating when things just never go my way.", 1),
    ]
]


@pytest.fixture()
def temp_folder() -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture(params=["lancedb", "milvus"])
def disconnected_repository(request, temp_folder) -> MemorysetRepository:
    match request.param:
        case "lancedb":
            return MemorysetLanceDBRepository(
                database_uri=f"{temp_folder}/lance.db",
                collection_name="memories",
            )
        case "milvus":
            return MemorysetMilvusRepository(
                database_uri=f"{temp_folder}/milvus.db",
                collection_name="memories",
            )
        case _:
            raise ValueError(f"Invalid storage backend: {request.param}")


@pytest.fixture()
def repository(disconnected_repository) -> MemorysetRepository:
    return disconnected_repository.connect(MEMORYSET_METADATA)


def test_config_collection(disconnected_repository):
    # When getting config for a new storage backend that has never been connected
    config = disconnected_repository.get_config()
    # Then the config is None
    assert config is None
    # When the storage backend is connected
    connected_repository = disconnected_repository.connect(MEMORYSET_METADATA)
    # Then the config is not None anymore
    config = connected_repository.get_config()
    assert config is not None
    for m in MEMORYSET_METADATA.__dict__.keys():
        assert getattr(config, m) == getattr(MEMORYSET_METADATA, m)
    # When reconnecting to the storage backend without connecting
    RepositoryImplementation = connected_repository.__class__
    database_uri = connected_repository.database_uri
    collection_name = connected_repository.collection_name
    del disconnected_repository
    del connected_repository
    reconnected_repository = RepositoryImplementation(database_uri=database_uri, collection_name=collection_name)
    # Then the config is not None
    config = reconnected_repository.get_config()
    assert config is not None


def test_reload_repository(repository):
    # Given a storage backend with some data
    repository.insert(TEXT_DATA)
    assert len(repository) == len(TEXT_DATA)
    RepositoryImplementation = repository.__class__
    database_uri = repository.database_uri
    collection_name = repository.collection_name
    del repository
    # When we reconnect to the storage backend
    reconnected_repository = RepositoryImplementation(
        database_uri=database_uri, collection_name=collection_name
    ).connect(MEMORYSET_METADATA)
    # Then we can access its memories
    assert len(reconnected_repository) == len(TEXT_DATA)


def test_drop_collection(repository):
    # Given a storage backend with some data
    repository.insert(TEXT_DATA)
    assert len(repository) == len(TEXT_DATA)
    # When we drop the storage backend
    repository.drop()
    # Then we can no longer access its memories
    with pytest.raises(RuntimeError):
        len(repository)
    # When we re instantiate the storage backend
    RepositoryImplementation = repository.__class__
    database_uri = repository.database_uri
    collection_name = repository.collection_name
    del repository
    reconnected_repository = RepositoryImplementation(database_uri=database_uri, collection_name=collection_name)
    # Then the storage backend does not exist anymore
    config = reconnected_repository.get_config()
    assert config is None
    # And it has no memories after reconnecting
    assert len(reconnected_repository.connect(MEMORYSET_METADATA)) == 0


def test_reset_repository(repository):
    # Given a storage backend with some data
    repository.insert(TEXT_DATA)
    assert len(repository) == len(TEXT_DATA)
    # When we reset the storage backend
    repository.reset(MEMORYSET_METADATA)
    # Then the storage backend is empty
    assert len(repository) == 0


def test_to_list(repository):
    # Given a storage backend with some data
    repository.insert(TEXT_DATA)
    assert len(repository) == len(TEXT_DATA)
    # When we get the list of memories
    values = repository.to_list()
    # Then we get a list of all the memories
    assert len(values) == len(TEXT_DATA)
    # And the memories have the correct value, embedding, and embedding shape and type
    for value in values:
        assert isinstance(value, LabeledMemory)
        assert isinstance(value.memory_id, str)
        assert isinstance(value.memory_version, int)
        assert isinstance(value.value, str)
        assert isinstance(value.embedding, np.ndarray)
        assert value.embedding.shape == (MEMORYSET_METADATA.embedding_dim,)
        assert value.embedding.dtype == np.float32


def test_get_by_id(repository):
    # Given a storage backend with some data
    repository.insert(TEXT_DATA)
    # When we get a memory by its memory_id
    memory = repository[TEXT_DATA[0]["memory_id"]]
    # Then we get the correct memory
    assert isinstance(memory, LabeledMemory)
    assert memory.value == TEXT_DATA[0]["text"]


def test_upsert(repository):
    # When we insert a memory
    repository.upsert(TEXT_DATA[0])
    # Then the memory is inserted
    assert len(repository) == 1
    # And the memory has the correct value
    assert repository[TEXT_DATA[0]["memory_id"]].value == TEXT_DATA[0]["text"]
    # When we update the memory
    repository.upsert(TEXT_DATA[0] | {"text": "updated_value", "label": 3, "memory_version": 2})
    # Then no new memory is inserted
    assert len(repository) == 1
    # And the memory has the updated value
    assert repository[TEXT_DATA[0]["memory_id"]].value == "updated_value"
    assert repository[TEXT_DATA[0]["memory_id"]].label == 3
    assert repository[TEXT_DATA[0]["memory_id"]].memory_version == 2


def test_delete(repository):
    # Given a storage backend with some data
    repository.insert(TEXT_DATA)
    assert len(repository) == len(TEXT_DATA)
    # When we delete a memory
    repository.delete(TEXT_DATA[0]["memory_id"])
    # Then the memory is deleted
    assert repository[TEXT_DATA[0]["memory_id"]] is None
    assert len(repository) == len(TEXT_DATA) - 1


def test_insert_and_lookup_text(repository):
    # Given a storage backend with some text memories
    repository.insert(TEXT_DATA)
    # And a query vector
    query = np.array(TEXT_DATA[0]["embedding"]).reshape(1, -1)
    # When we look up the query vector
    memory_lookups = repository.lookup(query, 4, use_cache=False)
    # Then we get a list of lists of memories
    assert isinstance(memory_lookups, list)
    assert len(memory_lookups) == 1
    assert isinstance(memory_lookups[0], list)
    assert len(memory_lookups[0]) == 4
    # And the first memory in the list is the one with the matching text
    assert isinstance(memory_lookups[0][0].value, str)
    assert memory_lookups[0][0].value == TEXT_DATA[0]["text"]
    # And the lookup score is high
    assert memory_lookups[0][0].lookup_score >= 0.99
    # And the embedding is a numpy array of the correct shape and type
    assert isinstance(memory_lookups[0][0].embedding, np.ndarray)
    assert memory_lookups[0][0].embedding.shape == (MEMORYSET_METADATA.embedding_dim,)
    assert memory_lookups[0][0].embedding.dtype == np.float32


def test_lookup_caching(repository):
    # Given a storage backend with some data
    repository.insert(TEXT_DATA)
    # When we lookup a few queries
    k = 4
    queries = np.array([m["embedding"] for m in TEXT_DATA])
    assert queries.shape == (8, MEMORYSET_METADATA.embedding_dim)
    memory_lookups = repository.lookup(queries, k, use_cache=True)
    assert len(memory_lookups) == len(queries)
    # Then the results are stored in the cache
    assert len(repository._cache) == len(queries)
    assert all(repository._cache.get(repository._get_cache_key(q, k)) is not None for q in queries)
    # When we lookup a subset of those queries again
    start = perf_counter()
    cached_memory_lookups = repository.lookup(queries[:6], k, use_cache=True)
    cached_duration = perf_counter() - start
    repository._cache.clear()
    assert len(repository._cache) == 0
    start = perf_counter()
    uncached_memory_lookups = repository.lookup(queries[:6], k, use_cache=True)
    uncached_duration = perf_counter() - start
    # Then the lookup is faster
    assert cached_duration < uncached_duration
    # And the cached results are the same as the uncached results
    assert all(
        all(
            cached_memory_lookups[i][j].value == uncached_memory_lookups[i][j].value
            for j in range(len(cached_memory_lookups[i]))
        )
        for i in range(len(cached_memory_lookups))
    )
    # When we make a lookup that can be resolved from the cache entirely
    assert all(repository._cache.get(repository._get_cache_key(q, k)) is not None for q in queries[:4])
    cached_memory_lookups = repository.lookup(queries[:4], k, use_cache=True)
    # Then it works as expected
    assert len(cached_memory_lookups) == 4


def test_insert_and_lookup_image(repository):
    # Given a storage backend with a few PNG images
    images = [
        Image.open(io.BytesIO(base64.b64decode(base64_string)))
        for base64_string in [
            "iVBORw0KGgoAAAANSUhEUgAAAAkAAAAJCAIAAABv85FHAAAAN0lEQVR4nGP8//8/Aw7AgmAyMkIZMNVM6BJIbCZ0CSRpJnRRJEBQDtOp//8j6UOWhrFZMIXgAABurQ8RDsBcHQAAAABJRU5ErkJggg==",  # red circle
            "iVBORw0KGgoAAAANSUhEUgAAAAkAAAAJCAIAAABv85FHAAAALUlEQVR4nGP8//8/Aw7AhMxhbGTEKYdTH0QTslYi9CErh7MJ6UNzHsJuPP4DANsWCaCKZRMuAAAAAElFTkSuQmCC",  # green triangle
            "iVBORw0KGgoAAAANSUhEUgAAAAkAAAAJCAIAAABv85FHAAAAKElEQVR4nM2PsQ0AMAyDcJX/XyYP1HtYEQNRKQyQfITyWgSn3ADtcAGzGQcROl7AigAAAABJRU5ErkJggg==",  # blue square
        ]
    ]
    repository.insert(
        [
            MemoryToInsert(
                text=None,
                label=i,
                label_name=None,
                metadata="{}",
                embedding=EmbeddingModel.CLIP_BASE.embed(image).tolist()[0],
                image=image,
                memory_version=1,
                memory_id=str(uuid.uuid4()),
            )
            for i, image in enumerate(images)
        ]
    )
    # When we look up the first image by its embedding
    memory_lookups = repository.lookup(EmbeddingModel.CLIP_BASE.embed(images[0]), 2, use_cache=False)
    # Then we get a list of lists of memories
    assert isinstance(memory_lookups, list)
    assert len(memory_lookups) == 1
    assert isinstance(memory_lookups[0], list)
    assert len(memory_lookups[0]) == 2
    # And the first memory in the list is the one with the matching image
    assert memory_lookups[0][0].label == 0
    # And the lookup score is high
    assert memory_lookups[0][0].lookup_score >= 0.99
    # And the image value is returned properly
    assert isinstance(memory_lookups[0][0].value, Image.Image)
    assert ImageChops.difference(memory_lookups[0][0].value, images[0]).getbbox() is None


def test_repository_equality():
    # Given two storage backends with the same database URI and collection name
    repository1 = MemorysetLanceDBRepository(database_uri="test", collection_name="test")
    repository2 = MemorysetLanceDBRepository(database_uri="test", collection_name="test")
    # And a repository of a different type
    repository3 = MemorysetMilvusRepository(database_uri="test", collection_name="test")
    # And a repository with a different database URI
    repository4 = MemorysetLanceDBRepository(database_uri="test2", collection_name="test")
    # And a repository with a different collection name
    repository5 = MemorysetMilvusRepository(database_uri="test", collection_name="test2")
    # Then the same repositories are equal
    assert repository1 == repository2
    # And different repositories are not equal
    assert repository1 != repository3
    assert repository1 != repository4
    assert repository1 != repository5
