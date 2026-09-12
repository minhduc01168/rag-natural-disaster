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
    print("Generating Figure 1: System Architecture...")
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    # Title & Subtitle
    ax.text(
        7.0,
        8.2,
        "TERRA: Tactical Emergency Retrieval-augmented Resilient Architecture",
        ha="center",
        va="center",
        fontsize=15,
        fontweight="bold",
        color="#0F172A",
    )
    ax.text(
        7.0,
        7.85,
        "Four-Stage Decoupled Pipeline for High-Stakes Mountain Disaster Operational Decision Support",
        ha="center",
        va="center",
        fontsize=10.5,
        fontstyle="italic",
        color="#475569",
    )

    # Box styles & palettes
    c_stage1 = "#EFF6FF"  # Blue tint - Ingestion
    c_stage1_b = "#2563EB"
    c_stage2 = "#F0FDF4"  # Green tint - Hybrid Retrieval
    c_stage2_b = "#16A34A"
    c_stage3 = "#FEF3C7"  # Amber tint - Re-ranking
    c_stage3_b = "#D97706"
    c_stage4 = "#FAF5FF"  # Purple tint - Generation
    c_stage4_b = "#9333EA"

    # Helper function for drawing rounded stage boxes
    def draw_stage(x, y, w, h, title, subtitle, bg_col, border_col):
        rect = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.15,rounding_size=0.2",
            facecolor=bg_col,
            edgecolor=border_col,
            linewidth=1.8,
        )
        ax.add_patch(rect)
        ax.text(
            x + w / 2,
            y + h - 0.35,
            title,
            ha="center",
            va="center",
            fontsize=11.5,
            fontweight="bold",
            color=border_col,
        )
        ax.text(
            x + w / 2,
            y + h - 0.7,
            subtitle,
            ha="center",
            va="center",
            fontsize=8.5,
            fontstyle="italic",
            color="#334155",
        )

    # Helper function for drawing sub-component cards
    def draw_card(
        x, y, w, h, title, details, bg="#FFFFFF", border="#94A3B8", text_c="#0F172A"
    ):
        rect = patches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.1,rounding_size=0.12",
            facecolor=bg,
            edgecolor=border,
            linewidth=1.1,
        )
        ax.add_patch(rect)
        ax.text(
            x + w / 2,
            y + h - 0.28,
            title,
            ha="center",
            va="center",
            fontsize=9.5,
            fontweight="bold",
            color=text_c,
        )
        ax.text(
            x + w / 2,
            y + (h - 0.28) / 2,
            details,
            ha="center",
            va="center",
            fontsize=8.0,
            color="#475569",
            linespacing=1.25,
        )

    # Helper function for arrow connectors
    def draw_arrow(
        x1, y1, x2, y2, label="", color="#475569", label_y_offset=0.25
    ):
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(
                arrowstyle="-|>",
                color=color,
                lw=1.8,
                mutation_scale=14,
                shrinkA=3,
                shrinkB=3,
            ),
        )
        if label:
            ax.text(
                (x1 + x2) / 2,
                (y1 + y2) / 2 + label_y_offset,
                label,
                ha="center",
                va="center",
                fontsize=8.0,
                fontweight="bold",
                color=color,
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#FFFFFF", edgecolor="none"),
            )

    # -------------------------------------------------------------
    # STAGE 1: Offline Knowledge Ingestion
    # -------------------------------------------------------------
    draw_stage(
        0.5,
        1.0,
        3.0,
        6.4,
        "STAGE 1: KNOWLEDGE INGESTION",
        "Two-Tier Structure-Preserving Chunking",
        c_stage1,
        c_stage1_b,
    )
    draw_card(
        0.7,
        5.6,
        2.6,
        1.0,
        "Authoritative Handbooks",
        "7 Mountain Disaster Manuals\nLaw 33/2013, QĐ 18/2021",
        bg="#FFFFFF",
        border=c_stage1_b,
    )
    draw_card(
        0.7,
        4.1,
        2.6,
        1.1,
        "Tier-1 Markdown Splitter",
        "Header depth H1-H4 tracking\nPreserves table & decree integrity",
        bg="#FFFFFF",
        border="#93C5FD",
    )
    draw_card(
        0.7,
        2.6,
        2.6,
        1.1,
        "Tier-2 Recursive Splitter",
        "Target length L = 1000 chars\nSliding overlap δ = 150 chars",
        bg="#FFFFFF",
        border="#93C5FD",
    )
    draw_card(
        0.7,
        1.2,
        2.6,
        1.0,
        "Dual Persistent Storage",
        "ChromaDB (Vector Store)\nIn-Memory BM25 Corpus Index",
        bg="#DBEAFE",
        border=c_stage1_b,
    )

    draw_arrow(2.0, 5.6, 2.0, 5.2)
    draw_arrow(2.0, 4.1, 2.0, 3.7)
    draw_arrow(2.0, 2.6, 2.0, 2.2)

    # -------------------------------------------------------------
    # USER QUERY INPUT BOX (Left to Stage 2)
    # -------------------------------------------------------------
    draw_card(
        4.0,
        7.1,
        2.6,
        0.85,
        "Operational User Query",
        "\"13 nhiệm vụ Chủ tịch xã về PCTT?\"\n(Mountain Command Query)",
        bg="#FEF2F2",
        border="#EF4444",
        text_c="#B91C1C",
    )

    # -------------------------------------------------------------
    # STAGE 2: Hybrid Dense-Lexical Retrieval & RRF
    # -------------------------------------------------------------
    draw_stage(
        3.9,
        1.0,
        3.0,
        5.7,
        "STAGE 2: HYBRID RETRIEVAL",
        "Dense-Sparse Fusion via RRF (k=60)",
        c_stage2,
        c_stage2_b,
    )
    draw_card(
        4.1,
        4.7,
        2.6,
        1.0,
        "Dense Retrieval Pathway",
        "Harrier-OSS-v1-0.6B (d=1024)\nChromaDB Cosine Sim (Top-10)",
        bg="#FFFFFF",
        border=c_stage2_b,
    )
    draw_card(
        4.1,
        3.3,
        2.6,
        1.0,
        "Lexical Retrieval Pathway",
        "BM25 Okapi with Viet Tokenizer\nExact Jargon & Legal Match (Top-10)",
        bg="#FFFFFF",
        border=c_stage2_b,
    )
    draw_card(
        4.1,
        1.3,
        2.6,
        1.5,
        "Reciprocal Rank Fusion",
        "RRF Score(d) = ∑ 1 / (60 + r_i)\nEliminates semantic bias\nFuses Top-10 candidates",
        bg="#DCFCE7",
        border=c_stage2_b,
    )

    draw_arrow(5.3, 7.1, 5.3, 5.7, label="Query Broadcast")
    draw_arrow(5.3, 5.7, 5.3, 5.7)
    # Connect Stage 1 Dual storage to Stage 2
    draw_arrow(3.3, 1.7, 4.1, 4.9, label="Passage Vectors", color="#2563EB")
    draw_arrow(3.3, 1.5, 4.1, 3.6, label="Inverted Index", color="#2563EB")
    draw_arrow(5.4, 4.7, 5.4, 4.3)
    draw_arrow(5.4, 3.3, 5.4, 2.8)

    # -------------------------------------------------------------
    # STAGE 3: Cross-Encoder Re-ranking
    # -------------------------------------------------------------
    draw_stage(
        7.3,
        1.0,
        3.0,
        6.4,
        "STAGE 3: CROSS-ENCODER",
        "Token-Level Cross-Attention",
        c_stage3,
        c_stage3_b,
    )
    draw_card(
        7.5,
        5.4,
        2.6,
        1.1,
        "Candidate Pool Input",
        "Top-10 Candidates from RRF\nFull query-passage concatenation",
        bg="#FFFFFF",
        border=c_stage3_b,
    )
    draw_card(
        7.5,
        3.4,
        2.6,
        1.5,
        "ms-marco-MiniLM-L-6-v2",
        "Full token-level interaction\nScore(q, p) = CrossAttn(q ∘ p)\nResolves keyword stuffing\nLatency: ~25ms per pool",
        bg="#FEF3C7",
        border=c_stage3_b,
    )
    draw_card(
        7.5,
        1.4,
        2.6,
        1.3,
        "Strict Top-K Selection",
        "Extracts Top-3 Gold Passages\nRejection threshold filtering\nContext Precision: 92.4%",
        bg="#FFFFFF",
        border=c_stage3_b,
    )

    draw_arrow(6.7, 2.0, 7.5, 5.7, label="Top-10 Pool", color="#16A34A")
    draw_arrow(8.8, 5.4, 8.8, 4.9)
    draw_arrow(8.8, 3.4, 8.8, 2.7)

    # -------------------------------------------------------------
    # STAGE 4: Grounded Multi-Agent LLM Generation
    # -------------------------------------------------------------
    draw_stage(
        10.6,
        1.0,
        3.0,
        6.4,
        "STAGE 4: SYNTHESIS LAYER",
        "Fact-Checked Decision Support",
        c_stage4,
        c_stage4_b,
    )
    draw_card(
        10.8,
        5.4,
        2.6,
        1.1,
        "Prompt Engine & Guardrail",
        "Context Injection (Top-3)\nStrict Grounding Constraint\n(Zero-Hallucination Policy)",
        bg="#FFFFFF",
        border=c_stage4_b,
    )
    draw_card(
        10.8,
        3.4,
        2.6,
        1.5,
        "Gemini 2.5 Flash Generator",
        "Operational Task Synthesis\nActionable Step Formulation\nLatency: 1.2s - 1.8s\nFaithfulness Score: 94.8%",
        bg="#F3E8FF",
        border=c_stage4_b,
    )
    draw_card(
        10.8,
        1.4,
        2.6,
        1.3,
        "Actionable Guidance",
        "Cited Legal Decrees (QĐ 18)\nExact 4-on-the-spot Actions\nEmergency Dispatch Contacts",
        bg="#FAF5FF",
        border=c_stage4_b,
    )

    draw_arrow(10.1, 2.0, 10.8, 5.7, label="Top-3 Contexts", color="#D97706")
    draw_arrow(12.1, 5.4, 12.1, 4.9)
    draw_arrow(12.1, 3.4, 12.1, 2.7)

    # Output arrow to user
    ax.text(
        12.1,
        0.55,
        "Verified Decision Output Delivered to Field Team",
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold",
        color="#15803D",
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
    ax1.set_ylim(40, 105)
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

    # Highlight delta arrow
    ax1.annotate(
        "+29.0%\nHit@1 Lift",
        xy=(2 - width, 87.0),
        xytext=(1 - width, 94.0),
        arrowprops=dict(facecolor="#DC2626", shrink=0.08, width=1.5, headwidth=6),
        ha="center",
        va="center",
        fontsize=9.0,
        fontweight="bold",
        color="#DC2626",
        bbox=dict(boxstyle="round,pad=0.2", facecolor="#FEF2F2", edgecolor="#DC2626", lw=0.8),
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
    ax.tick_params(axis="x", pad=18)

    ax.set_rlabel_position(25)
    plt.yticks(
        [40, 60, 80, 100],
        ["40%", "60%", "80%", "100%"],
        color="#64748B",
        size=8.5,
    )
    plt.ylim(30, 105)

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
    ax2.set_ylim(75, 105)
    ax2.grid(axis="y", linestyle="--", alpha=0.6)
    ax2.legend(loc="lower right", framealpha=0.9, fontsize=9.5)

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
