from emissor.persistence import ScenarioStorage
from emissor.persistence.persistence import ScenarioController
from emissor.processing.api import SignalProcessor
from emissor.representation.scenario import Modality, Signal
from emissor.representation.scenario import Annotation, Mention
from cltl.nlp.spacy_nlp import SpacyNLP
from cltl.nlp.api import NLP, Token, NamedEntity, Entity
from cltl.combot.infra.time_util import timestamp_now
import uuid
from itertools import chain
import argparse
import sys

class NLPAnnotator (SignalProcessor):

    def __init__(self, model):
        """ an evaluator that will use reference metrics to approximate the quality of a conversation, across turns.
        params
        returns: None
        """
        self._nlp= SpacyNLP(spacy_model=model)

    def process_signal(self, scenario: ScenarioController, text_signal: Signal):
        if not text_signal.modality == Modality.TEXT:
            return
        doc = self._nlp.analyze(text_signal.text)

        # TODO recap emissor Annotation classes -> NER, Token, etc.
        token_segments, token_annotations = self._convert_to_segment_annotation(text_signal, Token.__name__, doc.tokens)
        ner_segments, ner_annotations = self._convert_to_segment_annotation(text_signal, NamedEntity.__name__, doc.named_entities)
        entity_segments, entity_annotations = self._convert_to_segment_annotation(text_signal, Entity.__name__, doc.entities)

        mentions = [Mention(str(uuid.uuid4()), [segment], [annotation])
                    for segment, annotation
                    in chain(zip(token_segments, token_annotations),
                             zip(ner_segments, ner_annotations),
                             zip(entity_segments, entity_annotations))]
        text_signal.mentions.extend(mentions)

    def _convert_to_segment_annotation(self, text_signal, type, collection):
        annotations = [Annotation(type, element, NLP.__name__, timestamp_now()) for element in collection]
        segments = [text_signal.ruler.get_offset(*element.segment) for element in collection]

        return segments, annotations

def main(emissor_path:str, scenario:str,  model:str):
    annotator = NLPAnnotator(model=model)
    scenario_storage = ScenarioStorage(emissor_path)
    scenario_ctrl = scenario_storage.load_scenario(scenario)
    signals = scenario_ctrl.get_signals(Modality.TEXT)
    for signal in signals:
        annotator.process_signal(scenario=scenario_ctrl, text_signal=signal)
    #### Save the modified scenario to emissor
    scenario_storage.save_scenario(scenario_ctrl)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Statistical evaluation emissor scenario')
    parser.add_argument('--emissor-path', type=str, required=False, help="Path to the emissor folder", default='')
    parser.add_argument('--scenario', type=str, required=False, help="Identifier of the scenario", default='')
    parser.add_argument('--model', type=str, required=False, help="Spacy model used for processing", default='')

    args, _ = parser.parse_known_args()
    print('Input arguments', sys.argv)
    main(emissor_path=args.emissor_path,
         scenario=args.scenario,
         model=args.model)
