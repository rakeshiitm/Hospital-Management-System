import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import confusion_matrix, classification_report
import warnings
warnings.filterwarnings("ignore")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Medical PCA — Breast Cancer",
    page_icon="🔬",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252940);
        border: 1px solid #3a3f5c;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 6px 0;
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #7c9fff; }
    .metric-label { font-size: 0.85rem; color: #9aa0b8; margin-top: 4px; }
    .section-header {
        background: linear-gradient(90deg, #1e2130, transparent);
        border-left: 4px solid #7c9fff;
        padding: 10px 16px;
        border-radius: 0 8px 8px 0;
        margin: 24px 0 16px 0;
        font-size: 1.15rem;
        font-weight: 600;
        color: #e0e6ff;
    }
    .insight-box {
        background: #1a1f33;
        border: 1px solid #2e3450;
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 0.9rem;
        color: #b0b8d8;
        line-height: 1.6;
    }
    .tag {
        display: inline-block;
        background: #2a3060;
        color: #7c9fff;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.78rem;
        margin: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ── Load & cache data ─────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name="target")
    labels = {0: "Malignant", 1: "Benign"}
    return X, y, labels, data.feature_names

@st.cache_data
def run_pca(variance_threshold):
    X, y, labels, feature_names = load_data()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # PCA with threshold
    pca = PCA(n_components=variance_threshold)
    X_reduced = pca.fit_transform(X_scaled)

    # Full PCA for scree
    pca_full = PCA()
    pca_full.fit(X_scaled)

    return X_scaled, X_reduced, y.values, pca, pca_full, feature_names

@st.cache_data
def run_benchmarks(variance_threshold):
    X_scaled, X_reduced, y, pca, _, _ = run_pca(variance_threshold)
    cv = StratifiedKFold(n_splits=5, shuffle=False)
    results = {}
    for name, model in [("Logistic Regression", LogisticRegression(max_iter=10000, random_state=42)),
                         ("SVM", SVC(random_state=42))]:
        orig = cross_val_score(model, X_scaled, y, cv=cv, scoring="accuracy")
        red  = cross_val_score(model, X_reduced, y, cv=cv, scoring="accuracy")
        results[name] = {
            "original_mean":  orig.mean(),
            "original_std":   orig.std(),
            "reduced_mean":   red.mean(),
            "reduced_std":    red.std(),
        }
    return results

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    variance_threshold = st.slider(
        "Variance Retention Target",
        min_value=0.70, max_value=0.99, value=0.91, step=0.01,
        format="%.2f",
        help="PCA will auto-select the number of components needed to hit this threshold."
    )
    st.markdown("---")
    st.markdown("### 📊 Dataset Info")
    st.markdown("""
    <div class='insight-box'>
    <b>Wisconsin Breast Cancer Dataset</b><br><br>
    569 samples · 30 features<br>
    212 Malignant · 357 Benign<br><br>
    Features include cell nucleus measurements: radius, texture, perimeter, area, smoothness, etc.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 🏷️ Techniques Used")
    for tag in ["PCA", "StandardScaler", "Logistic Regression", "SVM", "5-Fold CV", "Scikit-learn"]:
        st.markdown(f"<span class='tag'>{tag}</span>", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
X_scaled, X_reduced, y, pca, pca_full, feature_names = run_pca(variance_threshold)
n_components = pca.n_components_
actual_variance = pca.explained_variance_ratio_.sum() * 100
feature_reduction = (1 - n_components / 30) * 100
benchmark_results = run_benchmarks(variance_threshold)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("# 🔬 Medical Dimensionality Reduction")
st.markdown("**PCA applied to breast cancer diagnosis — comparing model performance before and after feature reduction**")
st.markdown("---")

# ── Top metrics ───────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{n_components}</div>
        <div class='metric-label'>Components Selected</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{actual_variance:.1f}%</div>
        <div class='metric-label'>Variance Retained</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{feature_reduction:.0f}%</div>
        <div class='metric-label'>Feature Reduction</div>
    </div>""", unsafe_allow_html=True)
with c4:
    lr = benchmark_results["Logistic Regression"]
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{lr['reduced_mean']*100:.1f}%</div>
        <div class='metric-label'>LR Accuracy (Reduced)</div>
    </div>""", unsafe_allow_html=True)

# ── Section 1: Scree Plot + Cumulative Variance ───────────────────────────────
st.markdown("<div class='section-header'>📈 Scree Plot & Cumulative Variance</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(7, 4), facecolor="#0f1117")
    ax.set_facecolor("#0f1117")
    evr = pca_full.explained_variance_ratio_ * 100
    colors = ["#7c9fff" if i < n_components else "#3a3f5c" for i in range(30)]
    ax.bar(range(1, 31), evr, color=colors, edgecolor="none")
    ax.set_xlabel("Principal Component", color="#9aa0b8", fontsize=10)
    ax.set_ylabel("Explained Variance (%)", color="#9aa0b8", fontsize=10)
    ax.set_title("Scree Plot", color="#e0e6ff", fontsize=13, fontweight="bold", pad=12)
    ax.tick_params(colors="#9aa0b8")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2e3450")
    selected = mpatches.Patch(color="#7c9fff", label=f"Selected ({n_components} PCs)")
    dropped  = mpatches.Patch(color="#3a3f5c", label="Dropped")
    ax.legend(handles=[selected, dropped], facecolor="#1e2130", edgecolor="#3a3f5c",
              labelcolor="#e0e6ff", fontsize=9)
    st.pyplot(fig)
    plt.close()

with col2:
    fig, ax = plt.subplots(figsize=(7, 4), facecolor="#0f1117")
    ax.set_facecolor("#0f1117")
    cumvar = np.cumsum(pca_full.explained_variance_ratio_) * 100
    ax.plot(range(1, 31), cumvar, color="#7c9fff", linewidth=2.5, marker="o",
            markersize=4, markerfacecolor="#7c9fff")
    ax.axhline(y=variance_threshold * 100, color="#ff6b6b", linestyle="--",
               linewidth=1.5, label=f"Target: {variance_threshold*100:.0f}%")
    ax.axvline(x=n_components, color="#ffd166", linestyle="--",
               linewidth=1.5, label=f"Cutoff: PC {n_components}")
    ax.fill_between(range(1, 31), cumvar, alpha=0.1, color="#7c9fff")
    ax.set_xlabel("Number of Components", color="#9aa0b8", fontsize=10)
    ax.set_ylabel("Cumulative Variance (%)", color="#9aa0b8", fontsize=10)
    ax.set_title("Cumulative Explained Variance", color="#e0e6ff", fontsize=13,
                 fontweight="bold", pad=12)
    ax.tick_params(colors="#9aa0b8")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2e3450")
    ax.legend(facecolor="#1e2130", edgecolor="#3a3f5c", labelcolor="#e0e6ff", fontsize=9)
    st.pyplot(fig)
    plt.close()

# ── Section 2: 2D Scatter ─────────────────────────────────────────────────────
st.markdown("<div class='section-header'>🔵 2D Cluster Separation (PC1 vs PC2)</div>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    pca2 = PCA(n_components=2)
    X_2d = pca2.fit_transform(X_scaled)
    fig, ax = plt.subplots(figsize=(8, 5), facecolor="#0f1117")
    ax.set_facecolor("#0f1117")
    colors_map = {0: "#ff6b6b", 1: "#7c9fff"}
    label_map  = {0: "Malignant", 1: "Benign"}
    for cls in [0, 1]:
        mask = y == cls
        ax.scatter(X_2d[mask, 0], X_2d[mask, 1],
                   c=colors_map[cls], label=label_map[cls],
                   alpha=0.65, s=28, edgecolors="none")
    ax.set_xlabel(f"PC1 ({pca2.explained_variance_ratio_[0]*100:.1f}% variance)",
                  color="#9aa0b8", fontsize=10)
    ax.set_ylabel(f"PC2 ({pca2.explained_variance_ratio_[1]*100:.1f}% variance)",
                  color="#9aa0b8", fontsize=10)
    ax.set_title("PCA — 2D Projection of Breast Cancer Data", color="#e0e6ff",
                 fontsize=13, fontweight="bold", pad=12)
    ax.tick_params(colors="#9aa0b8")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2e3450")
    ax.legend(facecolor="#1e2130", edgecolor="#3a3f5c", labelcolor="#e0e6ff", fontsize=10)
    st.pyplot(fig)
    plt.close()

with col2:
    var1 = pca2.explained_variance_ratio_[0] * 100
    var2 = pca2.explained_variance_ratio_[1] * 100
    st.markdown(f"""
    <div class='insight-box'>
    <b>What this shows</b><br><br>
    Even with just <b>2 components</b> ({var1:.1f}% + {var2:.1f}% = {var1+var2:.1f}% variance), 
    the two classes are largely separable.<br><br>
    This confirms that the 30 original features carry <b>significant redundancy</b> — 
    most diagnostic information lives in a much lower-dimensional space.<br><br>
    The overlap region between clusters is where misclassifications typically occur.
    </div>
    """, unsafe_allow_html=True)

# ── Section 3: Model Benchmarks ───────────────────────────────────────────────
st.markdown("<div class='section-header'>🤖 Model Performance — Original vs PCA-Reduced</div>",
            unsafe_allow_html=True)

col1, col2 = st.columns(2)
model_names  = list(benchmark_results.keys())
orig_means   = [benchmark_results[m]["original_mean"] * 100 for m in model_names]
orig_stds    = [benchmark_results[m]["original_std"]  * 100 for m in model_names]
red_means    = [benchmark_results[m]["reduced_mean"]  * 100 for m in model_names]
red_stds     = [benchmark_results[m]["reduced_std"]   * 100 for m in model_names]

with col1:
    fig, ax = plt.subplots(figsize=(7, 4.5), facecolor="#0f1117")
    ax.set_facecolor("#0f1117")
    x = np.arange(len(model_names))
    w = 0.35
    bars1 = ax.bar(x - w/2, orig_means, w, yerr=orig_stds, label="Original (30 features)",
                   color="#7c9fff", capsize=5, error_kw={"ecolor": "#5a7fdf"})
    bars2 = ax.bar(x + w/2, red_means,  w, yerr=red_stds,  label=f"PCA-Reduced ({n_components} features)",
                   color="#ffd166", capsize=5, error_kw={"ecolor": "#ddb030"})
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{bar.get_height():.1f}%", ha="center", va="bottom",
                color="#e0e6ff", fontsize=9)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f"{bar.get_height():.1f}%", ha="center", va="bottom",
                color="#e0e6ff", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(model_names, color="#9aa0b8", fontsize=10)
    ax.set_ylabel("5-Fold CV Accuracy (%)", color="#9aa0b8", fontsize=10)
    ax.set_title("Accuracy Comparison", color="#e0e6ff", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylim([92, 102])
    ax.tick_params(colors="#9aa0b8")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2e3450")
    ax.legend(facecolor="#1e2130", edgecolor="#3a3f5c", labelcolor="#e0e6ff", fontsize=9)
    st.pyplot(fig)
    plt.close()

with col2:
    rows = []
    for m in model_names:
        r = benchmark_results[m]
        drop = r["original_mean"] - r["reduced_mean"]
        rows.append({
            "Model": m,
            "Original": f"{r['original_mean']*100:.2f}% ± {r['original_std']*100:.2f}%",
            "Reduced":  f"{r['reduced_mean'] *100:.2f}% ± {r['reduced_std'] *100:.2f}%",
            "Drop": f"{drop*100:.2f}%"
        })
    df_bench = pd.DataFrame(rows)
    st.dataframe(df_bench.set_index("Model"), use_container_width=True)

    st.markdown(f"""
    <div class='insight-box' style='margin-top:12px'>
    <b>Key Takeaway</b><br><br>
    With <b>{feature_reduction:.0f}% fewer features</b> ({30}→{n_components}), 
    accuracy drops by only <b>~{(benchmark_results['Logistic Regression']['original_mean'] - benchmark_results['Logistic Regression']['reduced_mean'])*100:.1f}%</b> for LR 
    and <b>~{(benchmark_results['SVM']['original_mean'] - benchmark_results['SVM']['reduced_mean'])*100:.1f}%</b> for SVM.<br><br>
    In real-world medical applications, this reduction means 
    <b>faster inference</b>, <b>lower storage</b>, and 
    <b>reduced measurement cost</b> — fewer cell attributes need to be measured per biopsy.
    </div>
    """, unsafe_allow_html=True)

# ── Section 4: Feature Loadings Heatmap ──────────────────────────────────────
st.markdown("<div class='section-header'>🧬 Feature Contributions to Principal Components</div>",
            unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    loadings = pd.DataFrame(
        pca.components_[:5],
        columns=feature_names,
        index=[f"PC{i+1}" for i in range(min(5, n_components))]
    )
    fig, ax = plt.subplots(figsize=(14, 3.5), facecolor="#0f1117")
    ax.set_facecolor("#0f1117")
    sns.heatmap(
        loadings, ax=ax, cmap="RdBu_r", center=0, linewidths=0.3,
        linecolor="#0f1117", annot=False, cbar_kws={"shrink": 0.8},
        xticklabels=[f.replace(" ", "\n") for f in feature_names],
    )
    ax.set_title("PCA Component Loadings (Top 5 PCs)", color="#e0e6ff",
                 fontsize=12, fontweight="bold", pad=10)
    ax.tick_params(axis="x", colors="#9aa0b8", labelsize=7, rotation=45)
    ax.tick_params(axis="y", colors="#9aa0b8", labelsize=9)
    st.pyplot(fig)
    plt.close()

with col2:
    top_features = loadings.abs().max().sort_values(ascending=False).head(6)
    st.markdown("<div class='insight-box'><b>Top Contributing Features</b><br><br>" +
                "".join([f"<span class='tag'>{f}</span> " for f in top_features.index]) +
                "<br><br>These features dominate variance across all principal components.</div>",
                unsafe_allow_html=True)

# ── Section 5: Raw Data Explorer ─────────────────────────────────────────────
with st.expander("📋 View Raw Dataset"):
    X_df, y_df, labels, _ = load_data()
    display_df = X_df.copy()
    display_df["Diagnosis"] = y_df.map({0: "Malignant", 1: "Benign"})
    st.dataframe(display_df.head(50), use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#4a5080; font-size:0.8rem;'>"
    "Dataset: Wisconsin Breast Cancer (sklearn) · "
    "Evaluation: 5-Fold Stratified CV · "
    "Built with Streamlit + scikit-learn"
    "</p>",
    unsafe_allow_html=True
)
