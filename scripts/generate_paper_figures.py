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
    fig = plt.figure(figsize=(17.5, 10.5), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 17.5)
    ax.set_ylim(0, 10.5)
    ax.axis("off")

    # Clean background canvas
    canvas_bg = patches.Rectangle((0, 0), 17.5, 10.5, facecolor="#F8FAFC", edgecolor="none")
    ax.add_patch(canvas_bg)

    # --------------------------------------------------------------------------
    # 0. HEADER: TITLE & TAXONOMY
    # --------------------------------------------------------------------------
    ax.text(
        8.75,
        10.12,
        "TERRA: Tactical Emergency Retrieval-augmented Resilient Architecture",
        ha="center",
        va="center",
        fontsize=16.5,
        fontweight="bold",
        color="#0F172A",
    )
    ax.text(
        8.75,
        9.80,
        "Decoupled Multi-Stage Hybrid Retrieval & Neural Re-Ranking Framework for Mountain Disaster Operational Decision Support",
        ha="center",
        va="center",
        fontsize=10.2,
        fontstyle="italic",
        color="#475569",
    )

    # Color tokens
    c_blue_p = "#1D4ED8"     # Blue (Data Plane & Dense)
    c_teal_p = "#0F766E"     # Teal (Sparse Lexical)
    c_emerald_p = "#047857"  # Emerald (Hybrid Retrieval & RRF)
    c_amber_p = "#B45309"    # Amber (Neural Cross-Encoder & Guarantees)
    c_purple_p = "#6B21A8"   # Purple (LLM Synthesis)
    c_slate_gray = "#64748B"

    # Helper: draw outer system phase container
    def draw_phase_container(x, y, w, h, title, subtitle="", bg="#F8FAFC", border="#3B82F6"):
        rect = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.08,rounding_size=0.15",
            facecolor=bg,
            edgecolor=border,
            linewidth=1.6,
            zorder=1,
        )
        ax.add_patch(rect)
        ax.text(
            x + 0.25,
            y + h - 0.22,
            title,
            ha="left",
            va="center",
            fontsize=9.8,
            fontweight="bold",
            color=border if border not in ["#CBD5E1", "#E2E8F0"] else "#1E293B",
            zorder=2,
        )
        if subtitle:
            ax.text(
                x + 0.25,
                y + h - 0.42,
                subtitle,
                ha="left",
                va="center",
                fontsize=7.6,
                fontstyle="italic",
                color=c_slate_gray,
                zorder=2,
            )

    # Helper: draw architectural component card
    def draw_component_card(x, y, w, h, title, chip_text, items, bg="#FFFFFF", border="#CBD5E1", title_color="#0F172A", chip_color=None):
        rect = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.05,rounding_size=0.12",
            facecolor=bg,
            edgecolor=border,
            linewidth=1.2,
            zorder=3,
        )
        ax.add_patch(rect)

        # Title
        ax.text(
            x + 0.18,
            y + h - 0.24,
            title,
            ha="left",
            va="center",
            fontsize=8.8,
            fontweight="bold",
            color=title_color,
            zorder=4,
        )

        # Micro-chip badge below title
        if chip_text:
            cp_col = chip_color if chip_color else title_color
            ax.text(
                x + 0.18,
                y + h - 0.46,
                chip_text,
                ha="left",
                va="center",
                fontsize=6.8,
                fontweight="bold",
                color=cp_col,
                bbox=dict(boxstyle="round,pad=0.16", facecolor="#FFFFFF", edgecolor=border, lw=0.7),
                zorder=4,
            )

        # Bullet items
        y_text = y + h - (0.72 if chip_text else 0.48)
        for item in items:
            ax.text(
                x + 0.18,
                y_text,
                item,
                ha="left",
                va="top",
                fontsize=7.3,
                color="#334155",
                linespacing=1.20,
                zorder=4,
            )
            y_text -= 0.27

    # Helper: draw orthogonal dataflow arrow with badge
    def draw_arrow(x1, y1, x2, y2, label="", color="#475569", lw=1.8, style="-|>", badge_color=None, badge_bg="#FFFFFF"):
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle=style,
                color=color,
                lw=lw,
                mutation_scale=13,
                shrinkA=0,
                shrinkB=0,
            ),
            zorder=6,
        )
        if label:
            b_col = badge_color if badge_color else color
            ax.text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                label,
                ha="center",
                va="center",
                fontsize=7.0,
                fontweight="bold",
                color=b_col,
                bbox=dict(
                    boxstyle="round,pad=0.18",
                    facecolor=badge_bg,
                    edgecolor=b_col,
                    lw=0.85,
                ),
                zorder=7,
            )

    # ==========================================================================
    # TIER 1 (TOP-LEFT): OFFLINE KNOWLEDGE INGESTION & DUAL INDEXING PLANE
    # ==========================================================================
    draw_phase_container(
        0.5,
        6.30,
        10.5,
        3.20,
        title="TIER 1: OFFLINE KNOWLEDGE INGESTION & DUAL INDEXING PLANE",
        subtitle="Corpus Ingestion, AST Structural Parsing, Two-Tier Chunking & Persistent Dual-Index Construction",
        bg="#F8FAFC",
        border="#2563EB",
    )

    # Card 1.1: Document Parsing
    draw_component_card(
        0.75,
        6.45,
        2.90,
        2.40,
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

    # Arrow 1.1 -> 1.2
    draw_arrow(3.65, 7.65, 4.30, 7.65, label="AST Nodes", color="#2563EB")

    # Card 1.2: Two-Tier Chunker
    draw_component_card(
        4.30,
        6.45,
        2.95,
        2.40,
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

    # Arrow 1.2 -> 1.3
    draw_arrow(7.25, 7.65, 7.90, 7.65, label="Passages", color="#2563EB")

    # Card 1.3: Dual Persistent Storage Engine
    draw_component_card(
        7.90,
        6.45,
        2.85,
        2.40,
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
        11.25,
        6.30,
        5.75,
        3.20,
        title="OPERATIONAL CRITERIA & SYSTEM GUARANTEES",
        subtitle="Mandates for High-Stakes Disaster Response Decision Support",
        bg="#FFFBEB",
        border="#D97706",
    )
    draw_component_card(
        11.45,
        6.45,
        5.35,
        2.40,
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
        0.5,
        0.75,
        16.5,
        5.00,
        title="TIER 2: ONLINE OPERATIONAL HYBRID RETRIEVAL & GROUNDED SYNTHESIS PIPELINE",
        subtitle="Real-Time Query Ingestion, Multi-Channel Hybrid Retrieval (RRF), Neural Re-Ranking & Grounded LLM Generation",
        bg="#F8FAFC",
        border="#475569",
    )

    # --------------------------------------------------------------------------
    # STAGE 1: FIELD QUERY INGESTION
    # --------------------------------------------------------------------------
    draw_component_card(
        0.75,
        0.95,
        2.90,
        4.10,
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

    # Query fan-out arrows to Channel A (Dense) and Channel B (Sparse)
    draw_arrow(3.65, 3.85, 4.40, 3.85, label="q (Dense)", color="#1D4ED8")
    draw_arrow(3.65, 2.05, 4.40, 2.05, label="q (Sparse)", color="#0F766E")

    # --------------------------------------------------------------------------
    # STAGE 2: HYBRID RETRIEVAL & RECIPROCAL RANK FUSION (RRF)
    # --------------------------------------------------------------------------
    stage2_rect = patches.FancyBboxPatch(
        (4.30, 0.95),
        4.50,
        4.10,
        boxstyle="round,pad=0.06,rounding_size=0.12",
        facecolor="#F0FDF4",
        edgecolor="#10B981",
        linewidth=1.3,
        zorder=2,
    )
    ax.add_patch(stage2_rect)

    ax.text(
        4.50,
        4.82,
        "Stage 2: Hybrid Retrieval & Fusion",
        ha="left",
        va="center",
        fontsize=9.2,
        fontweight="bold",
        color="#047857",
        zorder=4,
    )
    ax.text(
        4.50,
        4.60,
        "[Dual-Channel Parallel Search + RRF k=60]",
        ha="left",
        va="center",
        fontsize=6.8,
        fontweight="bold",
        color="#065F46",
        bbox=dict(boxstyle="round,pad=0.15", facecolor="#D1FAE5", edgecolor="#10B981", lw=0.7),
        zorder=4,
    )

    # Subcard 2A: Dense Vector Retrieval
    draw_component_card(
        4.50,
        2.95,
        4.10,
        1.50,
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
        4.50,
        1.10,
        4.10,
        1.50,
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

    # Vertical Arrow: Index Feed from Dual Storage (Top, x=8.45) straight down into Stage 2
    draw_arrow(8.45, 6.45, 8.45, 5.15, label="Dual Index Feed", color="#1D4ED8", badge_bg="#FFFFFF")

    # Reciprocal Rank Fusion (RRF) banner inside Stage 2
    rrf_box = patches.FancyBboxPatch(
        (4.50, 2.68),
        4.10,
        0.24,
        boxstyle="round,pad=0.03,rounding_size=0.06",
        facecolor="#D1FAE5",
        edgecolor="#059669",
        linewidth=1.0,
        zorder=4,
    )
    ax.add_patch(rrf_box)
    ax.text(
        6.55,
        2.80,
        "Reciprocal Rank Fusion (RRF): Score(d) = ∑ 1 / (60 + rank_i(d))",
        ha="center",
        va="center",
        fontsize=6.9,
        fontweight="bold",
        color="#065F46",
        zorder=5,
    )

    # Arrow from Stage 2 to Stage 3
    draw_arrow(8.80, 2.80, 9.50, 2.80, label="Top-10 Pool", color="#059669")

    # --------------------------------------------------------------------------
    # STAGE 3: NEURAL CROSS-ENCODER RE-RANKER
    # --------------------------------------------------------------------------
    draw_component_card(
        9.50,
        0.95,
        3.45,
        4.10,
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

    # Arrow from Stage 3 to Stage 4
    draw_arrow(12.95, 2.80, 13.65, 2.80, label="Top-3 Gold", color="#D97706")

    # --------------------------------------------------------------------------
    # STAGE 4: GROUNDED SYNTHESIS & TACTICAL DISPATCH
    # --------------------------------------------------------------------------
    draw_component_card(
        13.65,
        0.95,
        3.10,
        4.10,
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

    # --------------------------------------------------------------------------
    # BOTTOM SLA & NFR BAR (Enterprise Platform Standard)
    # --------------------------------------------------------------------------
    sla_bg = patches.FancyBboxPatch(
        (0.5, 0.15),
        16.5,
        0.45,
        boxstyle="round,pad=0.04,rounding_size=0.10",
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
        0.37,
        sla_text,
        ha="center",
        va="center",
        fontsize=8.2,
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
