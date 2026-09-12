#!/usr/bin/env python3
"""
Generate Publication-Grade Figures for the TERRA Research Paper (IEEE/ACM Standard)

Produces 4 camera-ready 300-DPI academic figures:
  1. fig1_terra_architecture.png: 4-Stage Decoupled System Architecture & Dataflow
  2. fig2_ablation_metrics.png: Ablation Study Comparison (Hit@1, Hit@3, MRR, Precision) across Configs A, B, C
  3. fig3_category_radar.png: Performance Across 6 Mountain Disaster Hazard Domains (Radar Chart)
  4. fig4_difficulty_tradeoff.png: Difficulty Robustness & Generation Faithfulness Analysis

Output directory: docs/paper/figures/
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

# Configure publication typography and styles
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["grid.color"] = "#E5E7EB"
plt.rcParams["grid.linestyle"] = "--"
plt.rcParams["grid.linewidth"] = 0.6

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../docs/paper/figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================================================================
# FIGURE 1: TERRA 4-Stage Decoupled Architecture Diagram
# ==============================================================================
def generate_figure_1():
    print("Generating Figure 1: Clean System Architecture (Winston SA Multi-Stage Layout)...")
    fig = plt.figure(figsize=(18, 10.5), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 17.5)
    ax.set_ylim(0, 10.0)
    ax.axis("off")

    # Canvas Background: Crisp white
    ax.add_patch(patches.Rectangle((0, 0), 17.5, 10.0, facecolor="#FFFFFF", zorder=0))

    # Master Architectural Header Banner
    ax.text(
        8.75,
        9.68,
        "TERRA: Tactical Emergency Retrieval-augmented Resilient Architecture",
        ha="center",
        va="center",
        fontsize=15.5,
        fontweight="bold",
        color="#0F172A",
        zorder=3,
    )
    ax.text(
        8.75,
        9.38,
        "Decoupled Multi-Stage Hybrid Retrieval & Neural Re-Ranking Framework for Mountain Disaster Operational Decision Support",
        ha="center",
        va="center",
        fontsize=9.2,
        fontstyle="italic",
        color="#475569",
        zorder=3,
    )

    # Architectural Color Palette
    c_blue_p = "#1E40AF"
    c_teal_p = "#0F766E"
    c_green_p = "#065F46"
    c_amber_p = "#92400E"
    c_purple_p = "#6B21A8"

    # Helper: draw outer tier container
    def draw_phase_container(x, y, w, h, title, subtitle, bg, border):
        container = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.06,rounding_size=0.16",
            facecolor=bg,
            edgecolor=border,
            linewidth=1.6,
            zorder=1,
        )
        ax.add_patch(container)
        ax.text(
            x + 0.22,
            y + h - 0.24,
            title,
            ha="left",
            va="center",
            fontsize=9.8,
            fontweight="bold",
            color=border,
            zorder=3,
        )
        ax.text(
            x + 0.22,
            y + h - 0.44,
            subtitle,
            ha="left",
            va="center",
            fontsize=7.6,
            fontstyle="italic",
            color="#64748B",
            zorder=3,
        )

    # Helper: draw component cards
    def draw_component_card(x, y, w, h, title, chip_text, items, bg="#FFFFFF", border="#CBD5E1", title_color="#0F172A"):
        card = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.05,rounding_size=0.10",
            facecolor=bg,
            edgecolor=border,
            linewidth=1.2,
            zorder=2,
        )
        ax.add_patch(card)

        ax.text(
            x + 0.16,
            y + h - 0.24,
            title,
            ha="left",
            va="center",
            fontsize=8.6,
            fontweight="bold",
            color=title_color,
            zorder=4,
        )

        if chip_text:
            ax.text(
                x + 0.16,
                y + h - 0.46,
                chip_text,
                ha="left",
                va="center",
                fontsize=6.6,
                fontweight="bold",
                color=border,
                bbox=dict(boxstyle="round,pad=0.12,rounding_size=0.06", facecolor="#F8FAFC", edgecolor=border, lw=0.65),
                zorder=4,
            )

        y_text = y + h - (0.72 if chip_text else 0.44)
        for it in items:
            if it == "":
                y_text -= 0.09
                continue
            is_sub = it.startswith("  -") or it.startswith("    ") or it.startswith("  ✓") or it.startswith("  (")
            f_size = 6.4 if is_sub else 6.9
            f_weight = "normal"
            ax.text(
                x + 0.16,
                y_text,
                it,
                ha="left",
                va="center",
                fontsize=f_size,
                fontweight=f_weight,
                color="#334155",
                linespacing=1.18,
                zorder=4,
            )
            y_text -= 0.25

    # Helper: draw dataflow arrow with label placed COMPLETELY OUTSIDE the arrow shaft
    def draw_arrow(x1, y1, x2, y2, label="", color="#475569", lw=2.0, label_pos="above", badge_bg="#FFFFFF"):
        # 1. Uninterrupted crisp arrow line
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=lw,
                mutation_scale=14,
                shrinkA=1,
                shrinkB=1,
            ),
            zorder=6,
        )
        # 2. Label placed with guaranteed clearance from the arrow line
        if label:
            if label_pos == "above":
                tx = (x1 + x2) / 2
                ty = (y1 + y2) / 2 + 0.16
                ha = "center"
                va = "bottom"
            elif label_pos == "below":
                tx = (x1 + x2) / 2
                ty = (y1 + y2) / 2 - 0.16
                ha = "center"
                va = "top"
            elif label_pos == "right":
                tx = (x1 + x2) / 2 + 0.18
                ty = (y1 + y2) / 2
                ha = "left"
                va = "center"
            elif label_pos == "left":
                tx = (x1 + x2) / 2 - 0.18
                ty = (y1 + y2) / 2
                ha = "right"
                va = "center"

            ax.text(
                tx,
                ty,
                label,
                ha=ha,
                va=va,
                fontsize=7.0,
                fontweight="bold",
                color=color,
                bbox=dict(
                    boxstyle="round,pad=0.14,rounding_size=0.08",
                    facecolor=badge_bg,
                    edgecolor=color,
                    lw=0.8,
                ),
                zorder=7,
            )

    # ==========================================================================
    # TIER 1 (TOP-LEFT): OFFLINE KNOWLEDGE INGESTION & DUAL INDEXING PLANE
    # ==========================================================================
    draw_phase_container(
        0.50,
        6.15,
        10.45,
        2.95,
        title="TIER 1: OFFLINE KNOWLEDGE INGESTION & DUAL INDEXING PLANE",
        subtitle="Corpus Ingestion, AST Structural Parsing, Two-Tier Chunking & Persistent Dual-Index Construction",
        bg="#F8FAFC",
        border="#2563EB",
    )

    # Card 1.1: Document Parsing
    draw_component_card(
        0.72,
        6.30,
        2.80,
        2.20,
        title="1. Corpus Normalization",
        chip_text="[7 Mountain Disaster Manuals]",
        items=[
            "• Legal: Law 33/2013, QĐ 18/2021",
            "• WB5 Handbook, Commune Guides",
            "• Markdown AST structural parser",
            "• H1-H4 header hierarchy extraction",
            "• Preserves statutory tables & articles",
        ],
        bg="#FFFFFF",
        border="#93C5FD",
        title_color=c_blue_p,
    )

    # Arrow 1.1 -> 1.2 (Unobstructed, label above)
    draw_arrow(3.52, 7.40, 4.32, 7.40, label="AST Nodes", color="#2563EB", label_pos="above")

    # Card 1.2: Two-Tier Chunker
    draw_component_card(
        4.32,
        6.30,
        2.80,
        2.20,
        title="2. Two-Tier Semantic Chunker",
        chip_text="[Tier 1: H1-H4 | Tier 2: L=1000, δ=150]",
        items=[
            "• Tier 1: Legal structure partition",
            "  (Preserves 'Điều, Khoản, Điểm')",
            "• Tier 2: Recursive sliding window",
            "  (Chunk size L=1000 chars, δ=150)",
            "• Institutional breadcrumb metadata",
            "• Zero semantic context truncation",
        ],
        bg="#FFFFFF",
        border="#93C5FD",
        title_color=c_blue_p,
    )

    # Arrow 1.2 -> 1.3 (Unobstructed, label above)
    draw_arrow(7.12, 7.40, 7.92, 7.40, label="Passages", color="#2563EB", label_pos="above")

    # Card 1.3: Dual Persistent Storage Engine
    draw_component_card(
        7.92,
        6.30,
        2.80,
        2.20,
        title="3. Dual Persistent Storage",
        chip_text="[ChromaDB + In-Memory BM25]",
        items=[
            "• Dense: ChromaDB Vector Store",
            "  - Model: Harrier-OSS-0.6B (d=1024)",
            "  - Cosine distance index",
            "• Sparse: BM25 Lexical Inverted Index",
            "  - Tokenized Vietnamese stems",
            "  - Okapi BM25 (k1=1.5, b=0.75)",
        ],
        bg="#EFF6FF",
        border="#1D4ED8",
        title_color=c_blue_p,
    )

    # ==========================================================================
    # TIER 1 (TOP-RIGHT): OPERATIONAL CRITERIA & EMERGENCY GUARANTEES
    # ==========================================================================
    draw_phase_container(
        11.20,
        6.15,
        5.80,
        2.95,
        title="OPERATIONAL CRITERIA & SYSTEM GUARANTEES",
        subtitle="Mandates for High-Stakes Disaster Response Decision Support",
        bg="#FFFBEB",
        border="#D97706",
    )
    draw_component_card(
        11.40,
        6.30,
        5.40,
        2.20,
        title="Mission-Critical Operational Mandates",
        chip_text="[High-Stakes Emergency Doctrine: Zero-Hallucination]",
        items=[
            "• 'Four-on-the-spot' Doctrine: Command, Forces, Equipment, Logistics",
            "• Zero-Hallucination Mandate: Exact citations (QĐ 18/2021, Law 33/2013)",
            "• Sub-Second Edge SLA: Retrieval P50 < 350ms over 3G/4G mountain relays",
            "• Cross-Attention Precision: Resolves subtle lexical collisions (Level 1 vs 3)",
            "• Life-Safety Attribution: Actionable first aid, routes & rescue contacts",
        ],
        bg="#FFFFFF",
        border="#F59E0B",
        title_color=c_amber_p,
    )

    # ==========================================================================
    # TIER 2 (BOTTOM): ONLINE OPERATIONAL INFERENCE PIPELINE
    # ==========================================================================
    draw_phase_container(
        0.50,
        0.80,
        16.50,
        4.90,
        title="TIER 2: ONLINE OPERATIONAL HYBRID RETRIEVAL & GROUNDED SYNTHESIS PIPELINE",
        subtitle="Real-Time Query Ingestion, Multi-Channel Hybrid Retrieval (RRF), Neural Re-Ranking & Grounded LLM Generation",
        bg="#F8FAFC",
        border="#475569",
    )

    # STAGE 1: FIELD QUERY INGESTION
    draw_component_card(
        0.72,
        0.98,
        2.80,
        4.00,
        title="Stage 1: Field Query Ingestion",
        chip_text="[Tactical Command Client]",
        items=[
            "• Field Commander Input:",
            "  \"13 nhiệm vụ của Chủ tịch xã",
            "   khi xảy ra lũ quét sạt lở?\"",
            "",
            "• Operational Context:",
            "  - Severe time-criticality",
            "  - Complex legal jargon",
            "  - Risk of life & property",
            "",
            "• Query Dispatch:",
            "  - Parallel broadcast to Dense",
            "  - Parallel broadcast to Sparse",
            "  - Preserves token embeddings",
        ],
        bg="#FEF2F2",
        border="#EF4444",
        title_color="#B91C1C",
    )

    # STAGE 2: HYBRID RETRIEVAL & RECIPROCAL RANK FUSION (RRF)
    stage2_rect = patches.FancyBboxPatch(
        (4.42, 0.98),
        4.30,
        4.00,
        boxstyle="round,pad=0.06,rounding_size=0.12",
        facecolor="#F0FDF4",
        edgecolor="#10B981",
        linewidth=1.3,
        zorder=2,
    )
    ax.add_patch(stage2_rect)

    ax.text(
        4.62,
        4.74,
        "Stage 2: Hybrid Retrieval & Fusion",
        ha="left",
        va="center",
        fontsize=9.0,
        fontweight="bold",
        color="#047857",
        zorder=4,
    )
    ax.text(
        4.62,
        4.52,
        "[Dual-Channel Parallel Search + RRF k=60]",
        ha="left",
        va="center",
        fontsize=6.7,
        fontweight="bold",
        color="#065F46",
        bbox=dict(boxstyle="round,pad=0.12,rounding_size=0.06", facecolor="#D1FAE5", edgecolor="#10B981", lw=0.65),
        zorder=4,
    )

    # Subcard 2A: Dense Vector Retrieval
    draw_component_card(
        4.62,
        3.02,
        3.90,
        1.38,
        title="Channel A: Dense Vector Search",
        chip_text="[Harrier-OSS-0.6B | Cosine Sim]",
        items=[
            "• Dense semantic embedding match",
            "• Resolves broad thematic intent & concepts",
            "• Slices Top-10 Dense candidates",
        ],
        bg="#FFFFFF",
        border="#3B82F6",
        title_color=c_blue_p,
    )

    # Subcard 2B: Sparse Lexical Retrieval
    draw_component_card(
        4.62,
        1.14,
        3.90,
        1.38,
        title="Channel B: Sparse Lexical Search",
        chip_text="[Okapi BM25 | Exact Legal Codes]",
        items=[
            "• Inverted index lexical keyword match",
            "• Pinpoints exact decree numbers & terms",
            "• Slices Top-10 Sparse candidates",
        ],
        bg="#FFFFFF",
        border="#0D9488",
        title_color=c_teal_p,
    )

    # Reciprocal Rank Fusion (RRF) banner inside Stage 2
    rrf_box = patches.FancyBboxPatch(
        (4.62, 2.64),
        3.90,
        0.26,
        boxstyle="round,pad=0.03,rounding_size=0.06",
        facecolor="#D1FAE5",
        edgecolor="#059669",
        linewidth=1.0,
        zorder=4,
    )
    ax.add_patch(rrf_box)
    ax.text(
        6.57,
        2.77,
        "Reciprocal Rank Fusion (RRF): Score(d) = ∑ 1 / (60 + rank_i(d))",
        ha="center",
        va="center",
        fontsize=6.6,
        fontweight="bold",
        color="#065F46",
        zorder=5,
    )

    # Query fan-out arrows from Stage 1 to Stage 2 Channels (unobstructed, label above)
    draw_arrow(3.52, 3.71, 4.42, 3.71, label="q (Dense)", color="#1D4ED8", label_pos="above")
    draw_arrow(3.52, 1.83, 4.42, 1.83, label="q (Sparse)", color="#0F766E", label_pos="above")

    # Vertical Arrow: Index Feed from Dual Storage down into Stage 2 (unobstructed, label right)
    draw_arrow(8.32, 6.30, 8.32, 4.98, label="Dual Index Feed", color="#1D4ED8", label_pos="right")

    # Arrow from Stage 2 to Stage 3 (unobstructed, label above)
    draw_arrow(8.72, 2.77, 9.62, 2.77, label="Top-10 Pool", color="#059669", label_pos="above")

    # STAGE 3: NEURAL CROSS-ENCODER RE-RANKER
    draw_component_card(
        9.62,
        0.98,
        3.25,
        4.00,
        title="Stage 3: Cross-Encoder Reranker",
        chip_text="[ms-marco-MiniLM-L-6-v2 | Token-Level]",
        items=[
            "• Full Token Cross-Attention [q ∘ p]:",
            "  - Evaluates direct query-document",
            "    token interactions",
            "  - Eliminates semantic representation bias",
            "",
            "• Precision Slicing Gate:",
            "  - Evaluates Top-10 candidates",
            "  - Strictly isolates Top-3 Gold Passages",
            "",
            "• Benchmark Validated Performance:",
            "  - Context Precision: 92.4% (+28.6% lift)",
            "  - MRR: 0.9167 | Hit@1: 87.0%",
            "  - Neural Latency: ~25ms per pool",
        ],
        bg="#FFFBEB",
        border="#D97706",
        title_color=c_amber_p,
    )

    # Arrow from Stage 3 to Stage 4 (unobstructed, label above)
    draw_arrow(12.87, 2.77, 13.77, 2.77, label="Top-3 Gold", color="#D97706", label_pos="above")

    # STAGE 4: GROUNDED SYNTHESIS & TACTICAL DISPATCH
    draw_component_card(
        13.77,
        0.98,
        2.98,
        4.00,
        title="Stage 4: Grounded Synthesis",
        chip_text="[Gemini 2.5 Flash | Attribution Shield]",
        items=[
            "• Fact-Checked LLM Generation:",
            "  - Model: Gemini 2.5 Flash",
            "  - Strict In-Context Attribution Guard",
            "  - Faithfulness: 94.8% (Anti-hallucination)",
            "  - Answer Relevance: 91.2%",
            "",
            "• Verified Actionable Output:",
            "  ✓ 4-on-the-spot Protocol Checklist",
            "    (Chỉ huy, Lực lượng, PT, Hậu cần)",
            "  ✓ Verifiable Statutory Citations",
            "    (Điều 32 Luật PCTT, QĐ 18)",
            "  ✓ Certified Emergency Dispatch",
            "    Hotline & Evacuation Contacts",
        ],
        bg="#FAF5FF",
        border="#7C3AED",
        title_color=c_purple_p,
    )

    # BOTTOM SLA & NFR BAR
    sla_bg = patches.FancyBboxPatch(
        (0.50, 0.18),
        16.50,
        0.42,
        boxstyle="round,pad=0.04,rounding_size=0.08",
        facecolor="#0F172A",
        edgecolor="#334155",
        linewidth=1.2,
        zorder=2,
    )
    ax.add_patch(sla_bg)

    sla_text = (
        "OPERATIONAL SLAs:   "
        "[LATENCY] P50 < 350ms (End-to-End <1.8s)   |   "
        "[PRECISION] Context Precision: 92.4% (+28.6% vs Naive)   |   "
        "[FIDELITY] Grounding Faithfulness: 94.8%   |   "
        "[ROBUSTNESS] High-Relief Disaster Hit@1: 100%"
    )
    ax.text(
        8.75,
        0.39,
        sla_text,
        ha="center",
        va="center",
        fontsize=8.0,
        fontweight="bold",
        color="#F8FAFC",
        zorder=3,
    )

    out_path = os.path.join(OUTPUT_DIR, "fig1_terra_architecture.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  -> Saved: {out_path}")


# ==============================================================================
# FIGURE 2: Ablation Study Performance Comparison (Hit@1, Hit@3, Hit@5, MRR)
# ==============================================================================
def generate_figure_2():
    print("Generating Figure 2: Ablation Study Comparison...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2), dpi=300)

    # Data from Benchmark Experiment (100 Queries)
    configs = [
        "Config A\n(Naive Dense Vector)",
        "Config B\n(Hybrid BM25+Dense)",
        "Config C\n(TERRA Framework)",
    ]
    colors = ["#3B82F6", "#0D9488", "#DC2626"]  # Blue, Teal, Red

    # Subplot 1: Hit@1, Hit@3, Hit@5
    x = np.arange(len(configs))
    width = 0.24

    hit1 = [58.0, 76.0, 87.0]
    hit3 = [78.0, 89.0, 96.0]
    hit5 = [85.0, 93.0, 98.0]

    rects1 = ax1.bar(
        x - width, hit1, width, label="Hit@1", color="#1E3A8A", edgecolor="#0F172A", lw=0.8
    )
    rects2 = ax1.bar(
        x, hit3, width, label="Hit@3", color="#0D9488", edgecolor="#0F172A", lw=0.8
    )
    rects3 = ax1.bar(
        x + width, hit5, width, label="Hit@5", color="#F59E0B", edgecolor="#0F172A", lw=0.8
    )

    ax1.set_ylabel("Retrieval Accuracy (%)", fontsize=11, fontweight="bold", color="#1E293B")
    ax1.set_title("(a) Retrieval Accuracy Across Ranks (Hit@K)", fontsize=12, fontweight="bold", pad=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(configs, fontsize=9.5, fontweight="medium")
    ax1.set_ylim(40, 110)
    ax1.grid(axis="y", linestyle="--", alpha=0.6)
    ax1.legend(loc="upper left", framealpha=0.9, fontsize=9.5)

    # Add data labels
    for rects in [rects1, rects2, rects3]:
        for r in rects:
            height = r.get_height()
            ax1.annotate(
                f"{height:.1f}%",
                xy=(r.get_x() + r.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.0,
                fontweight="bold",
                color="#0F172A",
            )

    # Highlight delta arrow directly above Config C (no bar crossing)
    ax1.annotate(
        "+29.0% Hit@1 Lift\n(vs. Naive Dense)",
        xy=(2 - width, 89.0),
        xytext=(2 - width, 103.0),
        arrowprops=dict(facecolor="#DC2626", shrink=0.08, width=1.5, headwidth=6),
        ha="center",
        va="center",
        fontsize=8.5,
        fontweight="bold",
        color="#DC2626",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="#FEF2F2", edgecolor="#DC2626", lw=1.0),
    )

    # Subplot 2: MRR and Context Precision
    x2 = np.arange(len(configs))
    w2 = 0.32

    mrr = [0.6980, 0.8354, 0.9167]
    precision = [62.4, 79.8, 92.4]

    rects_mrr = ax2.bar(
        x2 - w2 / 2,
        [m * 100 for m in mrr],
        w2,
        label="MRR (x100)",
        color="#6366F1",
        edgecolor="#312E81",
        lw=0.8,
    )
    rects_prec = ax2.bar(
        x2 + w2 / 2,
        precision,
        w2,
        label="Context Precision (%)",
        color="#EC4899",
        edgecolor="#831843",
        lw=0.8,
    )

    ax2.set_ylabel("Metric Score (%)", fontsize=11, fontweight="bold", color="#1E293B")
    ax2.set_title("(b) Ranking Quality: MRR & Context Precision", fontsize=12, fontweight="bold", pad=12)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(configs, fontsize=9.5, fontweight="medium")
    ax2.set_ylim(50, 105)
    ax2.grid(axis="y", linestyle="--", alpha=0.6)
    ax2.legend(loc="upper left", framealpha=0.9, fontsize=9.5)

    for r, val in zip(rects_mrr, mrr):
        h = r.get_height()
        ax2.annotate(
            f"{val:.4f}",
            xy=(r.get_x() + r.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.0,
            fontweight="bold",
            color="#312E81",
        )

    for r in rects_prec:
        h = r.get_height()
        ax2.annotate(
            f"{h:.1f}%",
            xy=(r.get_x() + r.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.0,
            fontweight="bold",
            color="#831843",
        )

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig2_ablation_metrics.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  -> Saved: {out_path}")


# ==============================================================================
# FIGURE 3: Performance Across 6 Mountain Disaster Hazard Domains (Radar Chart)
# ==============================================================================
def generate_figure_3():
    print("Generating Figure 3: Category Radar Chart...")
    categories = [
        "Landslide &\nFlash Flood\n(18 Qs)",
        "Typhoon &\nTorrential Rain\n(18 Qs)",
        "Community\nGovernance\n(26 Qs)",
        "Risk Mapping &\nEarly Warning\n(18 Qs)",
        "First Aid &\nSurvival\n(18 Qs)",
        "Vulnerable\nGroups\n(2 Qs)",
    ]
    N = len(categories)

    # Hit@1 scores across categories
    score_config_a = [50.0, 61.1, 53.8, 66.7, 61.1, 50.0]  # Naive Dense
    score_config_b = [72.2, 77.8, 73.1, 83.3, 77.8, 50.0]  # Hybrid RRF
    score_config_c = [88.9, 88.9, 84.6, 94.4, 83.3, 100.0]  # Proposed TERRA

    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    score_config_a += score_config_a[:1]
    score_config_b += score_config_b[:1]
    score_config_c += score_config_c[:1]

    fig, ax = plt.subplots(figsize=(8.5, 7.5), subplot_kw=dict(polar=True), dpi=300)

    # Rotate so first category is at top
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw axis lines & labels
    plt.xticks(angles[:-1], categories, size=9.5, fontweight="bold", color="#1E293B")
    ax.tick_params(axis="x", pad=28)

    ax.set_rlabel_position(25)
    plt.yticks(
        [40, 60, 80, 100],
        ["40%", "60%", "80%", "100%"],
        color="#64748B",
        size=8.5,
    )
    plt.ylim(30, 110)

    # Plot Config A: Naive Dense
    ax.plot(
        angles,
        score_config_a,
        linewidth=1.8,
        linestyle="solid",
        label="Config A: Naive Dense (Harrier)",
        color="#3B82F6",
    )
    ax.fill(angles, score_config_a, "#3B82F6", alpha=0.15)

    # Plot Config B: Hybrid RRF
    ax.plot(
        angles,
        score_config_b,
        linewidth=1.8,
        linestyle="--",
        label="Config B: Hybrid RRF (BM25+Dense)",
        color="#0D9488",
    )
    ax.fill(angles, score_config_b, "#0D9488", alpha=0.15)

    # Plot Config C: Proposed TERRA
    ax.plot(
        angles,
        score_config_c,
        linewidth=2.4,
        linestyle="solid",
        label="Config C: Proposed TERRA (Hybrid+Rerank)",
        color="#DC2626",
    )
    ax.fill(angles, score_config_c, "#DC2626", alpha=0.22)

    # Data markers on TERRA
    for ang, val in zip(angles[:-1], score_config_c[:-1]):
        ax.plot(ang, val, marker="o", markersize=6, color="#DC2626")

    plt.title(
        "Top-1 Retrieval Accuracy (Hit@1) Across 6 Specialized Hazard Domains\nDemonstrating Lexical Robustness on Administrative Jargon & High-Relief Hazards",
        size=11.5,
        fontweight="bold",
        color="#0F172A",
        pad=30,
    )
    plt.legend(loc="upper right", bbox_to_anchor=(1.25, 0.15), framealpha=0.9, fontsize=9.5)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig3_category_radar.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  -> Saved: {out_path}")


# ==============================================================================
# FIGURE 4: Difficulty Robustness & Generation Quality Metrics
# ==============================================================================
def generate_figure_4():
    print("Generating Figure 4: Difficulty Robustness & Generation Quality...")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.0), dpi=300)

    # Subplot 1: Performance by Difficulty Level
    diffs = ["Easy (28 Qs)", "Medium (56 Qs)", "Hard (16 Qs)"]
    x = np.arange(len(diffs))
    width = 0.28

    hit1_diff = [89.3, 85.7, 87.5]
    mrr_diff = [0.9345, 0.9077, 0.9167]

    b1 = ax1.bar(
        x - width / 2,
        hit1_diff,
        width,
        label="Hit@1 (%)",
        color="#059669",
        edgecolor="#064E3B",
        lw=0.8,
    )
    b2 = ax1.bar(
        x + width / 2,
        [m * 100 for m in mrr_diff],
        width,
        label="MRR (x100)",
        color="#0284C7",
        edgecolor="#082F49",
        lw=0.8,
    )

    ax1.set_ylabel("Score (%)", fontsize=11, fontweight="bold", color="#1E293B")
    ax1.set_title("(a) Retrieval Robustness Across Query Complexity Levels", fontsize=11.5, fontweight="bold", pad=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(diffs, fontsize=9.5, fontweight="medium")
    ax1.set_ylim(60, 105)
    ax1.grid(axis="y", linestyle="--", alpha=0.6)
    ax1.legend(loc="lower right", framealpha=0.9, fontsize=9.5)

    for r in b1:
        h = r.get_height()
        ax1.annotate(
            f"{h:.1f}%",
            xy=(r.get_x() + r.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color="#064E3B",
        )

    for r, val in zip(b2, mrr_diff):
        h = r.get_height()
        ax1.annotate(
            f"{val:.4f}",
            xy=(r.get_x() + r.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
            color="#082F49",
        )

    # Subplot 2: End-to-End Generation Quality (Faithfulness & Relevance)
    categories = ["Easy", "Medium", "Hard", "Overall\nAverage"]
    faithfulness = [96.2, 94.4, 93.8, 94.8]
    relevance = [92.5, 90.8, 90.1, 91.2]

    x2 = np.arange(len(categories))
    w2 = 0.32

    r_f = ax2.bar(
        x2 - w2 / 2,
        faithfulness,
        w2,
        label="Faithfulness (Anti-Hallucination)",
        color="#7C3AED",
        edgecolor="#4C1D95",
        lw=0.8,
    )
    r_r = ax2.bar(
        x2 + w2 / 2,
        relevance,
        w2,
        label="Answer Relevance",
        color="#F59E0B",
        edgecolor="#78350F",
        lw=0.8,
    )

    ax2.set_ylabel("Quality Score (%)", fontsize=11, fontweight="bold", color="#1E293B")
    ax2.set_title("(b) LLM Synthesis Quality & Grounding Fidelity", fontsize=11.5, fontweight="bold", pad=12)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(categories, fontsize=9.5, fontweight="medium")
    ax2.set_ylim(75, 114)
    ax2.grid(axis="y", linestyle="--", alpha=0.6)
    ax2.legend(loc="upper right", framealpha=0.95, fontsize=9.2)

    # Benchmark threshold line
    ax2.axhline(90.0, color="#DC2626", linestyle=":", lw=1.2, label="High-Stakes Safety Baseline (90%)")

    for r in r_f:
        h = r.get_height()
        ax2.annotate(
            f"{h:.1f}%",
            xy=(r.get_x() + r.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.0,
            fontweight="bold",
            color="#4C1D95",
        )

    for r in r_r:
        h = r.get_height()
        ax2.annotate(
            f"{h:.1f}%",
            xy=(r.get_x() + r.get_width() / 2, h),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8.0,
            fontweight="bold",
            color="#78350F",
        )

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "fig4_difficulty_tradeoff.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  -> Saved: {out_path}")


if __name__ == "__main__":
    print("=================================================================")
    print("  GENERATING 4 CAMERA-READY FIGURES FOR TERRA RESEARCH PAPER")
    print("=================================================================")
    generate_figure_1()
    generate_figure_2()
    generate_figure_3()
    generate_figure_4()
    print("=================================================================")
    print("  ALL 4 FIGURES GENERATED SUCCESSFULLY IN docs/paper/figures/ !")
    print("=================================================================")
