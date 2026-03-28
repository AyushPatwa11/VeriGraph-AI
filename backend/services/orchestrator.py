from services.fact_checker import FactChecker
from services.fusion_engine import FusionEngine
from services.gnn_analyzer import GNNAnalyzer
from services.graph_builder import GraphBuilder
from services.nlp_analyzer import NLPAnalyzer
from services.scraper import ScraperService


class Orchestrator:
    def __init__(self) -> None:
        self.scraper = ScraperService()
        self.graph_builder = GraphBuilder()
        self.nlp = NLPAnalyzer()
        self.gnn = GNNAnalyzer()
        self.fact_checker = FactChecker()
        self.fusion = FusionEngine()

    async def analyze(self, query: str):
        posts = await self.scraper.collect(query)

        nodes, links, metrics = self.graph_builder.build(posts)

        nlp_result = self.nlp.analyze(query, posts)
        gnn_result = self.gnn.analyze(nodes, links, metrics)
        gemini_result = await self.fact_checker.analyze(query)

        return self.fusion.fuse(
            query=query,
            nlp_result=nlp_result,
            gnn_result=gnn_result,
            gemini_result=gemini_result,
            nodes=nodes,
            links=links,
            posts=posts,
        )
