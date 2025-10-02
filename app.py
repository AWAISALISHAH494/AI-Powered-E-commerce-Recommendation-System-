import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
import os
from datetime import datetime
import random

# Configure page
st.set_page_config(
    page_title="🛍️ AI E-commerce Recommender",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database for user behavior tracking
def init_db():
    conn = sqlite3.connect('user_behavior.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            product_id INTEGER,
            product_name TEXT,
            interaction_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Load and cache product data
@st.cache_data
def load_products():
    try:
        return pd.read_csv("products.csv")
    except FileNotFoundError:
        st.error("products.csv not found. Please ensure the file exists in the project directory.")
        return pd.DataFrame()

# Build recommendation model
@st.cache_data
def build_recommendation_model(products_df):
    if products_df.empty:
        return None, None
    
    # Combine name, category, and description for better recommendations
    products_df['combined_features'] = (
        products_df['name'] + ' ' + 
        products_df['category'] + ' ' + 
        products_df['description']
    )
    
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=5000,
        ngram_range=(1, 2)
    )
    
    tfidf_matrix = vectorizer.fit_transform(products_df['combined_features'])
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    return vectorizer, similarity_matrix

# Content-based recommendation function
def get_content_recommendations(product_name, products_df, similarity_matrix, n=5):
    if product_name not in products_df['name'].values:
        return []
    
    idx = products_df[products_df['name'] == product_name].index[0]
    scores = list(enumerate(similarity_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
    # Get top N similar products (excluding the input product itself)
    top_indices = [i[0] for i in scores[1:n+1]]
    recommendations = products_df.iloc[top_indices].copy()
    recommendations['similarity_score'] = [scores[i+1][1] for i in range(len(top_indices))]
    
    return recommendations

# User behavior-based recommendations
def get_user_behavior_recommendations(user_id, products_df, n=5):
    conn = sqlite3.connect('user_behavior.db')
    
    # Get user's interaction history
    query = '''
        SELECT product_id, product_name, COUNT(*) as interaction_count
        FROM user_interactions 
        WHERE user_id = ?
        GROUP BY product_id, product_name
        ORDER BY interaction_count DESC, timestamp DESC
    '''
    
    user_history = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    
    if user_history.empty:
        # Return popular products for new users
        return products_df.sample(n=n)
    
    # Get categories of products the user has interacted with
    user_product_ids = user_history['product_id'].tolist()
    user_categories = products_df[products_df['id'].isin(user_product_ids)]['category'].unique()
    
    # Recommend products from similar categories that user hasn't seen
    unseen_products = products_df[
        (~products_df['id'].isin(user_product_ids)) & 
        (products_df['category'].isin(user_categories))
    ]
    
    if len(unseen_products) >= n:
        return unseen_products.sample(n=n)
    else:
        # Fill remaining slots with random products
        remaining = n - len(unseen_products)
        other_products = products_df[~products_df['id'].isin(user_product_ids)].sample(n=remaining)
        return pd.concat([unseen_products, other_products])

# Log user interaction
def log_interaction(user_id, product_id, product_name, interaction_type):
    conn = sqlite3.connect('user_behavior.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_interactions (user_id, product_id, product_name, interaction_type)
        VALUES (?, ?, ?, ?)
    ''', (user_id, product_id, product_name, interaction_type))
    conn.commit()
    conn.close()

# Display product card
def display_product_card(product, show_similarity=False, key_namespace=""):
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            try:
                st.image(product['image_url'], width=150)
            except:
                st.image("https://via.placeholder.com/150x150?text=No+Image", width=150)
        
        with col2:
            st.subheader(f"**{product['name']}**")
            st.write(f"**Category:** {product['category']}")
            st.write(f"**Price:** ${product['price']}")
            
            if show_similarity and 'similarity_score' in product:
                st.write(f"**Match Score:** {product['similarity_score']:.2%}")
            
            # Ensure expander key uniqueness as well
            expander_key = f"desc_{key_namespace}_{product['id']}" if key_namespace else f"desc_{product['id']}"
            with st.expander("Product Description", expanded=False):
                st.write(product['description'])
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                view_key = f"view_{key_namespace}_{product['id']}" if key_namespace else f"view_{product['id']}"
                if st.button(f"👀 View Details", key=view_key):
                    log_interaction(st.session_state.user_id, product['id'], product['name'], 'view')
                    st.success("Added to your viewing history!")
            
            with col_btn2:
                cart_key = f"cart_{key_namespace}_{product['id']}" if key_namespace else f"cart_{product['id']}"
                if st.button(f"🛒 Add to Cart", key=cart_key):
                    log_interaction(st.session_state.user_id, product['id'], product['name'], 'add_to_cart')
                    st.success("Added to cart!")

# Main application
def main():
    # Initialize database
    init_db()
    
    # Initialize user session
    if 'user_id' not in st.session_state:
        st.session_state.user_id = f"user_{random.randint(1000, 9999)}"
    
    # Load data
    products_df = load_products()
    if products_df.empty:
        st.stop()
    
    # Build recommendation model
    vectorizer, similarity_matrix = build_recommendation_model(products_df)
    if similarity_matrix is None:
        st.error("Failed to build recommendation model.")
        st.stop()
    
    # Header
    st.title("🛍️ AI-Powered E-commerce Recommendation System")
    st.markdown("*Discover products tailored just for you using advanced machine learning*")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Recommendation Options")
        
        recommendation_type = st.radio(
            "Choose recommendation method:",
            ["Content-Based", "User Behavior", "Hybrid"]
        )
        
        num_recommendations = st.slider(
            "Number of recommendations:",
            min_value=3,
            max_value=10,
            value=5
        )
        
        st.markdown("---")
        st.markdown(f"**Your User ID:** `{st.session_state.user_id}`")
        
        # Display user stats
        conn = sqlite3.connect('user_behavior.db')
        user_stats = pd.read_sql_query(
            "SELECT COUNT(*) as total_interactions FROM user_interactions WHERE user_id = ?",
            conn, params=(st.session_state.user_id,)
        )
        conn.close()
        
        st.metric("Your Interactions", user_stats['total_interactions'].iloc[0])
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["🔍 Product Search", "⭐ Recommendations", "📊 Your Activity"])
    
    with tab1:
        st.header("Search Products")
        
        # Search functionality
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input("Search for products:", placeholder="e.g., iPhone, running shoes, books...")
        with col2:
            category_filter = st.selectbox("Category:", ["All"] + list(products_df['category'].unique()))
        
        # Filter products
        filtered_products = products_df.copy()
        
        if search_query:
            mask = (
                filtered_products['name'].str.contains(search_query, case=False, na=False) |
                filtered_products['description'].str.contains(search_query, case=False, na=False) |
                filtered_products['category'].str.contains(search_query, case=False, na=False)
            )
            filtered_products = filtered_products[mask]
        
        if category_filter != "All":
            filtered_products = filtered_products[filtered_products['category'] == category_filter]
        
        # Display search results
        if not filtered_products.empty:
            st.write(f"Found {len(filtered_products)} products:")
            
            for idx, product in filtered_products.iterrows():
                display_product_card(product, key_namespace="search")
                st.markdown("---")
        else:
            st.info("No products found. Try different search terms.")
    
    with tab2:
        st.header("Personalized Recommendations")
        
        if recommendation_type == "Content-Based":
            st.subheader("🎯 Content-Based Recommendations")
            
            selected_product = st.selectbox(
                "Select a product to get similar recommendations:",
                products_df['name'].values
            )
            
            if st.button("Get Recommendations", type="primary"):
                recommendations = get_content_recommendations(
                    selected_product, products_df, similarity_matrix, num_recommendations
                )
                
                if not recommendations.empty:
                    st.success(f"Products similar to **{selected_product}**:")
                    
                    for idx, product in recommendations.iterrows():
                        display_product_card(product, show_similarity=True, key_namespace="content")
                        st.markdown("---")
                else:
                    st.warning("No recommendations found.")
        
        elif recommendation_type == "User Behavior":
            st.subheader("👤 Behavior-Based Recommendations")
            st.info("Based on your viewing and purchase history")
            
            if st.button("Get Personal Recommendations", type="primary"):
                recommendations = get_user_behavior_recommendations(
                    st.session_state.user_id, products_df, num_recommendations
                )
                
                st.success("Recommended for you:")
                for idx, product in recommendations.iterrows():
                    display_product_card(product, key_namespace="behavior")
                    st.markdown("---")
        
        else:  # Hybrid
            st.subheader("🔄 Hybrid Recommendations")
            st.info("Combining content similarity and your personal preferences")
            
            col1, col2 = st.columns(2)
            with col1:
                selected_product = st.selectbox(
                    "Select a product for content-based:",
                    products_df['name'].values,
                    key="hybrid_product"
                )
            
            if st.button("Get Hybrid Recommendations", type="primary"):
                # Get half content-based, half behavior-based
                content_recs = get_content_recommendations(
                    selected_product, products_df, similarity_matrix, num_recommendations // 2
                )
                behavior_recs = get_user_behavior_recommendations(
                    st.session_state.user_id, products_df, num_recommendations - len(content_recs)
                )
                
                st.success("Hybrid recommendations combining similarity and your preferences:")
                
                if not content_recs.empty:
                    st.write("**Similar to your selection:**")
                    for idx, product in content_recs.iterrows():
                        display_product_card(product, show_similarity=True, key_namespace="hybrid_content")
                        st.markdown("---")
                
                if not behavior_recs.empty:
                    st.write("**Based on your preferences:**")
                    for idx, product in behavior_recs.iterrows():
                        display_product_card(product, key_namespace="hybrid_behavior")
                        st.markdown("---")
    
    with tab3:
        st.header("Your Activity Dashboard")
        
        # Load user activity
        conn = sqlite3.connect('user_behavior.db')
        user_activity = pd.read_sql_query('''
            SELECT product_name, interaction_type, timestamp, COUNT(*) as count
            FROM user_interactions 
            WHERE user_id = ?
            GROUP BY product_name, interaction_type
            ORDER BY timestamp DESC
        ''', conn, params=(st.session_state.user_id,))
        conn.close()
        
        if not user_activity.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Recent Activity")
                st.dataframe(user_activity[['product_name', 'interaction_type', 'count']])
            
            with col2:
                st.subheader("Activity Summary")
                activity_summary = user_activity.groupby('interaction_type')['count'].sum()
                st.bar_chart(activity_summary)
        else:
            st.info("No activity yet. Start exploring products to see your personalized dashboard!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🤖 Powered by AI • Built with Streamlit & scikit-learn</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
