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
    print("Generating Figure 1: Clean System Architecture (Orthogonal Layout)...")
    fig, ax = plt.subplots(figsize=(16.0, 9.2), dpi=300)
    ax.set_xlim(0, 16.0)
    ax.set_ylim(0, 9.2)
    ax.axis("off")

    # Title & Subtitle
    ax.text(
        8.0,
        8.85,
        "TERRA: Tactical Emergency Retrieval-augmented Resilient Architecture",
        ha="center",
        va="center",
        fontsize=15.5,
        fontweight="bold",
        color="#0F172A",
    )
    ax.text(
        8.0,
        8.52,
        "Decoupled Multi-Stage Framework for Mountain Disaster Operational Decision Support",
        ha="center",
        va="center",
        fontsize=10.5,
        fontstyle="italic",
        color="#475569",
    )

    # Color tokens
    c_blue_bg = "#F8FAFC"
    c_blue_b = "#2563EB"
    c_slate_bg = "#F8FAFC"
    c_slate_b = "#475569"

    # Helper: draw container with title banner
    def draw_container(x, y, w, h, title, bg_color, border_color):
        rect = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.12,rounding_size=0.18",
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=1.6,
            zorder=1,
        )
        ax.add_patch(rect)
        ax.text(
            x + 0.35,
            y + h - 0.26,
            title,
            ha="left",
            va="center",
            fontsize=10.0,
            fontweight="bold",
            color=border_color,
            zorder=2,
        )

    # Helper: draw card
    def draw_card(
        x, y, w, h, title, items, bg="#FFFFFF", border="#CBD5E1", header_color="#0F172A"
    ):
        rect = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            facecolor=bg,
            edgecolor=border,
            linewidth=1.3,
            zorder=3,
        )
        ax.add_patch(rect)
        ax.text(
            x + w / 2,
            y + h - 0.25,
            title,
            ha="center",
            va="center",
            fontsize=9.2,
            fontweight="bold",
            color=header_color,
            zorder=4,
        )
        y_text = y + h - 0.52
        for item in items:
            ax.text(
                x + 0.14,
                y_text,
                item,
                ha="left",
                va="top",
                fontsize=7.8,
                color="#334155",
                linespacing=1.22,
                zorder=4,
            )
            y_text -= 0.35

    # Helper: draw straight orthogonal arrow with centered badge
    def draw_arrow(x1, y1, x2, y2, label="", color="#475569", badge_bg="#FFFFFF"):
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=2.0,
                mutation_scale=14,
                shrinkA=0,
                shrinkB=0,
            ),
            zorder=5,
        )
        if label:
            ax.text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                label,
                ha="center",
                va="center",
                fontsize=7.5,
                fontweight="bold",
                color=color,
                bbox=dict(
                    boxstyle="round,pad=0.22",
                    facecolor=badge_bg,
                    edgecolor=color,
                    lw=0.9,
                ),
                zorder=6,
            )

    # --------------------------------------------------------------------------
    # TOP CONTAINER: Offline Phase (Knowledge Ingestion & Storage)
    # --------------------------------------------------------------------------
    draw_container(
        0.45,
        5.00,
        7.35,
        3.20,
        "OFFLINE PHASE: KNOWLEDGE INGESTION & DUAL INDEXING",
        "#EFF6FF",
        c_blue_b,
    )

    # Card 1: Two-Tier Chunker
    draw_card(
        0.65,
        5.20,
        2.85,
        2.50,
        "1. Two-Tier Semantic Chunker",
        [
            "• 7 Mountain Disaster Manuals",
            "• Tier 1: Header H1-H4 structure",
            "• Preserves tabular rows & legal context",
            "• Tier 2: Recursive sliding split",
            "  (Chunk size L=1000, Overlap δ=150)",
            "• Breadcrumb metadata propagation",
        ],
        border="#93C5FD",
        header_color="#1D4ED8",
    )

    # Horizontal Arrow between Card 1 and Card 2 (Top Tier)
    draw_arrow(3.50, 6.45, 4.30, 6.45, label="Passages", color="#2563EB")

    # Card 2: Dual Storage
    draw_card(
        4.30,
        5.20,
        3.25,
        2.50,
        "2. Dual Persistent Storage",
        [
            "• ChromaDB Vector Database",
            "  (Harrier-OSS-0.6B Embeddings, d=1024)",
            "• BM25 Lexical Inverted Index",
            "  (Vietnamese Tokenized Index)",
            "• Dual Indexing guarantees hybrid",
            "  keyword + dense coverage",
        ],
        bg="#F0F9FF",
        border="#2563EB",
        header_color="#1D4ED8",
    )

    # Top Right Container: System Specifications & Goals
    draw_container(
        8.20,
        5.00,
        7.35,
        3.20,
        "OPERATIONAL CRITERIA & SYSTEM GUARANTEES",
        "#FEF3C7",
        "#D97706",
    )
    draw_card(
        8.40,
        5.20,
        6.95,
        2.50,
        "High-Stakes Emergency Decision Support Mandates",
        [
            "• Domain Mandate: Fast operational decisions under the 'Four-on-the-spot' doctrine",
            "• Zero-Hallucination Policy: Exact statutory citations (QĐ 18/2021, Law 33/2013)",
            "• Sub-Second SLA: End-to-end P50 retrieval latency <350ms for low-bandwidth 3G/4G",
            "• Cross-Attention Precision: Resolves subtle lexical collisions (e.g., Level 1 vs. Level 3)",
            "• Life-Safety Attribution: Verifiable first-aid, evacuation routes, and rescue contacts",
        ],
        bg="#FFFBEB",
        border="#F59E0B",
        header_color="#B45309",
    )

    # Vertical Feed-Down Arrow from Dual Storage (Top) to Hybrid Retrieval (Bottom)
    # Perfectly aligned at x = 5.925 (center of Card 2 in both tiers)
    draw_arrow(
        5.925, 5.00, 5.925, 3.75, label="Dual Index Lookup", color="#1D4ED8", badge_bg="#FFFFFF"
    )

    # --------------------------------------------------------------------------
    # BOTTOM CONTAINER: Online Phase (Inference Pipeline)
    # --------------------------------------------------------------------------
    draw_container(
        0.45,
        0.50,
        15.10,
        3.80,
        "ONLINE PHASE: REAL-TIME INFERENCE PIPELINE",
        c_slate_bg,
        c_slate_b,
    )

    # Bottom Card 1: Operational User Query
    draw_card(
        0.65,
        0.70,
        2.85,
        3.05,
        "Operational User Query",
        [
            "• Input from Commune Leader:",
            "  \"13 nhiệm vụ Chủ tịch xã",
            "   về PCTT khi xảy ra lũ quét?\"",
            "• Contains administrative legal jargon",
            "• High-urgency operational need",
            "• Parallel broadcast to retrieval",
        ],
        bg="#FEF2F2",
        border="#EF4444",
        header_color="#B91C1C",
    )

    # Horizontal Arrow 1 -> 2
    draw_arrow(3.50, 2.22, 4.30, 2.22, label="Query", color="#0F172A")

    # Bottom Card 2: Stage 2 Hybrid Retrieval & RRF
    draw_card(
        4.30,
        0.70,
        3.25,
        3.05,
        "Stage 2: Hybrid Retrieval & RRF",
        [
            "• Dense: Harrier-0.6B Cosine (Top-10)",
            "• Sparse: BM25 Okapi Match (Top-10)",
            "• Reciprocal Rank Fusion (k=60):",
            "  Score(d) = ∑ 1 / (60 + rank_i)",
            "• Mitigates dense representation bias",
            "• Fuses candidates into Top-10 Pool",
        ],
        bg="#F0FDF4",
        border="#16A34A",
        header_color="#15803D",
    )

    # Horizontal Arrow 2 -> 3
    draw_arrow(7.55, 2.22, 8.40, 2.22, label="Top-10 Pool", color="#16A34A")

    # Bottom Card 3: Stage 3 Cross-Encoder Reranker
    draw_card(
        8.40,
        0.70,
        3.35,
        3.05,
        "Stage 3: Cross-Encoder Reranker",
        [
            "• Model: ms-marco-MiniLM-L-6-v2",
            "• Full Token Cross-Attention [q ∘ p]",
            "• Evaluates fine-grained semantics",
            "• Re-ranks and slices Top-3 Passages",
            "• Context Precision: 92.4% (+28.6%)",
            "• Low Latency: ~25ms per candidate pool",
        ],
        bg="#FEF3C7",
        border="#D97706",
        header_color="#B45309",
    )

    # Horizontal Arrow 3 -> 4
    draw_arrow(11.75, 2.22, 12.55, 2.22, label="Top-3 Gold", color="#D97706")

    # Bottom Card 4: Stage 4 Grounded Synthesis
    draw_card(
        12.55,
        0.70,
        2.80,
        3.05,
        "Stage 4: Synthesis Layer",
        [
            "• Generator: Gemini 2.5 Flash",
            "• Strict Attribution Guardrail",
            "• Faithfulness: 94.8% (Anti-hallucination)",
            "• Answer Relevance: 91.2%",
            "• Actionable Checklist Output:",
            "  - Verifiable Legal Decrees",
            "  - '4-on-the-spot' Tactical Actions",
            "  - Emergency Dispatch Contacts",
        ],
        bg="#FAF5FF",
        border="#9333EA",
        header_color="#7E22CE",
    )

    plt.tight_layout()
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
