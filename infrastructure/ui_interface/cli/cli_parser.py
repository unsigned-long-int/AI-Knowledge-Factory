import argparse
import queue

from threading import Event, Thread
from dataclasses import dataclass
from typing import Dict, Any

from core.knowledge.ai_knowledge_factory_service import (
    AIKnowledgeFactory,
    InvalidCollector,
    NonRegisteredCollector
)
from core.query.response_provider import ResponseProviderError
from infrastructure.event_orchestration_service.event_orchestrator import EventOrchestrator
from infrastructure.event_orchestration_service.events import events

from .loading_spinner import spin
from .stdin_streamer import read_stdin_stream


@dataclass
class CLIParser:
    ai_knowledge_factory: AIKnowledgeFactory
    prog_name: str
    description: str
    default_context_size: int

    def process_query(self, event_orchestrator: EventOrchestrator) -> None:
        parser = self._setup_parser()
        args = parser.parse_args()
        user_query = args.query

        if not args.query:
            user_query = read_stdin_stream()

        progress_queue = queue.Queue()
        progress_queue.put('providing response...')

        done = Event()
        spinner = Thread(target=spin, args=(progress_queue, done))
        spinner.start()
        try:
            result = self.ai_knowledge_factory.provide_response(
                progress_queue=progress_queue,
                query=user_query,
                context_size=args.context_size
            )
            print(result.choices[0].message)
        except (InvalidCollector, NonRegisteredCollector) as e:
            event = events.CollectorInvokeFailed(str(e))
            event_orchestrator.queue.append(event)
        except ResponseProviderError as e:
            event = events.ResponseFetchingFailed(str(e))
            event_orchestrator.queue.append(event)
        except Exception as e:
            event = events.AIFactoryGenericExceptionEncountered(str(e))
            event_orchestrator.queue.append(event)
        finally:
            done.set()
            spinner.join()

    def _setup_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog=self.prog_name,
            description=self.description,
            formatter_class=argparse.MetavarTypeHelpFormatter
        )

        parser.add_argument(
            '-q',
            '--query',
            type=str,
            help='Your question which will be used to invoke dynamic information collection service to enrich it with the most relevant available information'
        )

        parser.add_argument(
            '-s',
            '--context_size',
            type=int,
            default=self.default_context_size,
            help='The desired size of the additional context information which the query will be enriched with'
        )

        return parser
