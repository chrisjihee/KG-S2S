import logging
from dataclasses import dataclass
from pathlib import Path

import jsonlines
from chrisbase.io import num_lines, LoggingFormat, configure_unit_logger
from chrisbase.util import mute_tqdm_cls
from dataclasses_json import DataClassJsonMixin

tqdm = mute_tqdm_cls()
logger = logging.getLogger(__name__)
configure_unit_logger(fmt=LoggingFormat.CHECK_12)


@dataclass
class WikidataFreebaseID(DataClassJsonMixin):
    wikidata_id: str
    freebase_id: str
    label1: str
    label2: str
    title1: str
    title2: str
    descr1: str
    descr2: str


@dataclass
class WikipediaDefinition(DataClassJsonMixin):
    page_id: int
    query: str
    title: str
    definition: str


existing_dir = Path('data/raw/FB15k-237')
changing_dir = Path('data/raw/FB15k-237-ko')
changing_dir.mkdir(parents=True, exist_ok=True)

mapping_file = Path('data/raw/Wiki-ko/wikidata-20230920-freebase.jsonl')
defining_file = Path('data/raw/Wiki-ko/wikipedia-20230920-definition.jsonl')
entities_file = existing_dir / "entities.txt"
entity2text_file = existing_dir / "entity2text.txt"
relation2text_file = existing_dir / "relation2text.txt"
entity2textlong_file = existing_dir / "entity2textlong.txt"

assert existing_dir.exists() and existing_dir.is_dir()
assert changing_dir.exists() and changing_dir.is_dir()
assert mapping_file.exists() and mapping_file.is_file()
assert defining_file.exists() and defining_file.is_file()
assert entities_file.exists() and entities_file.is_file()
assert entity2text_file.exists() and entity2text_file.is_file()
assert relation2text_file.exists() and relation2text_file.is_file()
assert entity2textlong_file.exists() and entity2textlong_file.is_file()
logger.info(f"Existing dir: {existing_dir}")
logger.info(f"Changing dir: {changing_dir}")
logger.info(f"Mapping file: {mapping_file}")
logger.info(f"Defining file: {defining_file}")

with jsonlines.open(mapping_file) as reader:
    progress, interval = (
        tqdm(reader, total=num_lines(mapping_file), unit="line", pre="*", desc="loading"),
        100_000,
    )
    mapping_to_freebase = dict()
    for i, x in enumerate(progress):
        if i > 0 and i % interval == 0:
            logger.info(progress)
        mapping = WikidataFreebaseID.from_dict(x)
        mapping_to_freebase[mapping.freebase_id] = mapping
    logger.info(progress)
logger.info(f"#mapping_to_freebase: {len(mapping_to_freebase)}")

with jsonlines.open(defining_file) as reader:
    progress, interval = (
        tqdm(reader, total=num_lines(defining_file), unit="line", pre="*", desc="loading"),
        100_000,
    )
    mapping_to_definition = dict()
    for i, x in enumerate(progress):
        if i > 0 and i % interval == 0:
            logger.info(progress)
        mapping = WikipediaDefinition.from_dict(x)
        mapping_to_definition[mapping.title] = mapping.definition
    logger.info(progress)
logger.info(f"#mapping_to_definition: {len(mapping_to_definition)}")

with entities_file.open() as reader:
    existing_entities = [x.strip() for x in reader]
with entity2text_file.open() as reader:
    existing_entity2text = dict(x.strip().split("\t") for x in reader)
with entity2textlong_file.open() as reader:
    existing_entity2textlong = dict(x.strip().split("\t") for x in reader)
with relation2text_file.open() as reader:
    existing_relation2text = dict(x.strip().split("\t") for x in reader)

changing_entities = [
    x for x in existing_entities if x in mapping_to_freebase
]
changing_entity2text = {
    x: (
        mapping_to_freebase[x].title1 if mapping_to_freebase[x].title1
        else mapping_to_freebase[x].title2 if mapping_to_freebase[x].title2
        else y
    )
    for x, y in existing_entity2text.items() if x in mapping_to_freebase
}
changing_entity2textlong = {
    x: (
        mapping_to_definition[mapping_to_freebase[x].title1]
        if mapping_to_freebase[x].title1 and mapping_to_freebase[x].title1 in mapping_to_definition
        else mapping_to_freebase[x].descr1 if mapping_to_freebase[x].descr1
        else mapping_to_freebase[x].descr2 if mapping_to_freebase[x].descr2
        else y
    )
    for x, y in existing_entity2textlong.items() if x in mapping_to_freebase
}

logger.info(f"#entities: {len(existing_entities)} -> {len(changing_entities)}")
logger.info(f"#entity2text: {len(existing_entity2text)} -> {len(changing_entity2text)}")
logger.info(f"#entity2textlong: {len(existing_entity2textlong)} -> {len(changing_entity2textlong)}")

with (changing_dir / entities_file.name).open("w") as writer:
    writer.writelines([
        x + "\n"
        for x in sorted(changing_entities)
    ])
logger.info(f"Saved to [{changing_dir / entities_file.name}]")

with (changing_dir / entity2text_file.name).open("w") as writer:
    writer.writelines([
        x + "\t" + changing_entity2text[x] + "\n"
        for x in sorted(list(changing_entity2text.keys()))
    ])
logger.info(f"Saved to [{changing_dir / entity2text_file.name}]")

with (changing_dir / entity2textlong_file.name).open("w") as writer:
    writer.writelines([
        x + "\t" + changing_entity2textlong[x] + "\n"
        for x in sorted(list(changing_entity2textlong.keys()))
    ])
logger.info(f"Saved to [{changing_dir / entity2textlong_file.name}]")

data_splits = ["train", "dev", "test"]
changing_relation2text = dict()
for data_split in data_splits:
    existing_file = existing_dir / f"{data_split}.tsv"
    changing_file = changing_dir / f"{data_split}.tsv"
    assert existing_file.exists() and existing_file.is_file()
    with existing_file.open() as reader:
        progress, interval = (
            tqdm(reader, total=num_lines(existing_file), unit="line", pre="*", desc="loading"),
            50_000,
        )
        changing_triples = list()
        for i, x in enumerate(progress):
            if i > 0 and i % interval == 0:
                logger.info(progress)
            head, rel, tail = x.strip().split("\t")
            if head in changing_entities and head in changing_entity2text and head in changing_entity2textlong:
                if tail in changing_entities and tail in changing_entity2text and tail in changing_entity2textlong:
                    changing_relation2text[rel] = existing_relation2text[rel]
                    changing_triples.append([head, rel, tail])
        logger.info(progress)
        logger.info(f"#triples ({data_split}): {num_lines(existing_file)} -> {len(changing_triples)}")
        with changing_file.open("w") as writer:
            writer.writelines([
                "\t".join(x) + "\n"
                for x in sorted(changing_triples)
            ])
        logger.info(f"Saved to [{changing_file}]")

logger.info(f"#relation2text: {len(existing_relation2text)} -> {len(changing_relation2text)}")
with (changing_dir / relation2text_file.name).open("w") as writer:
    writer.writelines([
        x + "\t" + changing_relation2text[x] + "\n"
        for x in sorted(list(changing_relation2text.keys()))
    ])
logger.info(f"Saved to [{changing_dir / relation2text_file.name}]")
