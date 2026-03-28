"use client";

import { useEffect, useRef, useState } from "react";
import * as d3 from "d3";
import { motion } from "framer-motion";
import type { GraphLink, GraphNode } from "@/types/analysis";
import { DEFAULT_GRAPH_NODES, DEFAULT_GRAPH_LINKS } from "@/lib/graph-fallback";

interface NetworkGraphProps {
  nodes: GraphNode[];
  links: GraphLink[];
}

type SimNode = d3.SimulationNodeDatum & GraphNode;
type SimLink = d3.SimulationLinkDatum<SimNode> & GraphLink;

const clusterColors = ["#58d3ff", "#7df5c5", "#ffd479", "#ff8f7e"];

function linkColor(kind: GraphLink["kind"]) {
  if (kind === "semantic") return "#59d4ff";
  if (kind === "temporal") return "#f8be5f";
  return "#ff7d6b";
}

export function NetworkGraph({ nodes, links }: NetworkGraphProps) {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [selected, setSelected] = useState<GraphNode | null>(null);

  useEffect(() => {
    if (!svgRef.current || !containerRef.current) return;

    // Determine if we're using fallback data (both nodes and links should match)
    const nodesAreEmpty = !nodes || nodes.length === 0;
    const linksAreEmpty = !links || links.length === 0;
    
    // Use fallback for BOTH if nodes are empty, otherwise use the provided ones
    const displayNodes = nodesAreEmpty ? DEFAULT_GRAPH_NODES : nodes;
    const displayLinks = nodesAreEmpty ? DEFAULT_GRAPH_LINKS : (linksAreEmpty ? [] : links);

    // Create simulation nodes and links with proper ID mapping
    const simNodes: SimNode[] = displayNodes.map((n) => ({ ...n }));
    
    // Map and filter links, only keeping those with valid source and target nodes
    const simLinkData = displayLinks.map((l) => {
      const sourceNode = simNodes.find(n => n.id === l.source);
      const targetNode = simNodes.find(n => n.id === l.target);
      
      if (sourceNode && targetNode) {
        return {
          ...l,
          source: sourceNode,
          target: targetNode,
        };
      }
      return null;
    });
    
    const simLinks: SimLink[] = simLinkData.filter((l) => l !== null) as SimLink[];

    const width = containerRef.current.clientWidth;
    const height = 400;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();
    svg.attr("width", width).attr("height", height);

    const simulation = d3
      .forceSimulation(simNodes)
      .force(
        "link",
        d3
          .forceLink<SimNode, SimLink>(simLinks)
          .distance(90)
          .strength(0.35)
      )
      .force("charge", d3.forceManyBody().strength(-180))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force(
        "collision",
        d3.forceCollide<SimNode>().radius((d: SimNode) => 10 + Math.sqrt(d.followers) / 9)
      );

    const linkSel = svg
      .append("g")
      .attr("stroke-width", 1.6)
      .selectAll<SVGLineElement, SimLink>("line")
      .data(simLinks)
      .join("line")
      .attr("stroke", (d: SimLink) => linkColor(d.kind))
      .attr("stroke-opacity", 0.8);

    const nodeSel = svg
      .append("g")
      .selectAll<SVGCircleElement, SimNode>("circle")
      .data(simNodes)
      .join("circle")
      .attr("r", (d: SimNode) => 8 + Math.sqrt(d.followers) / 18)
      .attr("fill", (d: SimNode) => clusterColors[d.cluster % clusterColors.length])
      .attr("stroke", "#0d1f2a")
      .attr("stroke-width", 2)
      .style("cursor", "pointer")
      .on("click", (_event: MouseEvent, d: SimNode) => setSelected(d))
      .call(
        d3
          .drag<SVGCircleElement, SimNode>()
          .on("start", (event: d3.D3DragEvent<SVGCircleElement, SimNode, SimNode>, d: SimNode) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event: d3.D3DragEvent<SVGCircleElement, SimNode, SimNode>, d: SimNode) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event: d3.D3DragEvent<SVGCircleElement, SimNode, SimNode>, d: SimNode) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );

    const labelSel = svg
      .append("g")
      .selectAll<SVGTextElement, SimNode>("text")
      .data(simNodes)
      .join("text")
      .text((d: SimNode) => d.label)
      .attr("font-size", 10)
      .attr("fill", "#e6f3f9")
      .attr("dx", 10)
      .attr("dy", 4)
      .style("pointer-events", "none");

    simulation.on("tick", () => {
      linkSel
        .attr("x1", (d: SimLink) => (d.source as SimNode).x ?? 0)
        .attr("y1", (d: SimLink) => (d.source as SimNode).y ?? 0)
        .attr("x2", (d: SimLink) => (d.target as SimNode).x ?? 0)
        .attr("y2", (d: SimLink) => (d.target as SimNode).y ?? 0);

      nodeSel.attr("cx", (d: SimNode) => d.x ?? 0).attr("cy", (d: SimNode) => d.y ?? 0);
      labelSel.attr("x", (d: SimNode) => d.x ?? 0).attr("y", (d: SimNode) => d.y ?? 0);
    });

    return () => {
      simulation.stop();
    };
  }, [nodes, links]);

  return (
    <section 
      className="rounded-3xl border border-white/15 bg-white/10 p-6 backdrop-blur-xl"
      aria-label="Account coordination network showing relationships between accounts"
      role="region"
    >
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className="text-xs uppercase tracking-[0.2em] text-[#97d4ee]">Coordination Network</p>
        <p className="text-xs text-[#9fbfd0]">Drag nodes • Click for details</p>
      </div>

      <div ref={containerRef} className="mt-4 h-96 rounded-2xl border border-white/10 bg-[#081b25] relative group">
        <svg ref={svgRef} className="h-full w-full" />
        
        {/* Legend Panel */}
        <motion.div 
          className="absolute top-4 left-4 rounded-lg border border-white/20 bg-white/[0.08] backdrop-blur-xl p-3 z-10"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <p className="text-xs font-semibold text-[#96c9df] mb-2">Network Legend</p>
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded-full bg-[#58d3ff]" />
              <span className="text-xs text-[#9fbfd0]">Account Node</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-1 w-4 bg-[#59d4ff]" />
              <span className="text-xs text-[#9fbfd0]">Semantic Link</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-1 w-4 bg-[#f8be5f]" />
              <span className="text-xs text-[#9fbfd0]">Temporal Link</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-1 w-4 bg-[#ff7d6b]" />
              <span className="text-xs text-[#9fbfd0]">URL Link</span>
            </div>
          </div>
        </motion.div>
      </div>

      {selected ? (
        <motion.aside
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 rounded-2xl border border-white/15 bg-[#0b2532] p-4 text-sm text-[#d6ebf6]"
        >
          <p className="font-semibold text-white">{selected.label}</p>
          <p className="mt-1 text-xs text-[#96c9df]">Followers: {selected.followers.toLocaleString()}</p>
          <p className="mt-1 text-xs text-[#96c9df]">Cluster: {selected.cluster}</p>
        </motion.aside>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-4 text-center text-xs text-[#96c9df]"
        >
          Click on any node to view account details
        </motion.div>
      )}
    </section>
  );
}
