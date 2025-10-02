# 🛍️ AI-Powered E-commerce Recommendation System

A smart e-commerce recommendation engine built with Python, Streamlit, and scikit-learn that suggests products based on content similarity and user behavior patterns.

## 🌟 Features

- **Content-Based Filtering**: Recommends products similar to what you're viewing using TF-IDF and cosine similarity
- **User Behavior Tracking**: Learns from your interactions to provide personalized recommendations
- **Hybrid Recommendations**: Combines both approaches for better accuracy
- **Interactive UI**: Clean, modern interface with product cards and images
- **Real-time Analytics**: Track your activity and preferences
- **SQLite Integration**: Persistent storage for user behavior data

## 🚀 Live Demo

[View Live App on Streamlit Cloud](https://your-app-url.streamlit.app) *(Deploy to get your URL)*

## 📋 Dataset

The system includes 25 sample products across multiple categories:
- Electronics (iPhone, MacBook, Cameras, etc.)
- Footwear (Nike, Adidas, Converse)
- Clothing (Jeans, T-shirts, Blazers)
- Books (Fiction, Programming, Self-help)
- Sports Equipment (Yoga mats, Dumbbells)
- Home Appliances (Kitchen gadgets, Cleaning tools)

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Frontend | Streamlit | Interactive web interface |
| Backend | Python | Core application logic |
| ML Engine | scikit-learn | TF-IDF vectorization & cosine similarity |
| Database | SQLite | User behavior tracking |
| Deployment | Streamlit Cloud | Free hosting platform |

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ecommerce-recommender.git
   cd ecommerce-recommender
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 🔧 How It Works

### 1. Content-Based Filtering
- Combines product name, category, and description into feature vectors
- Uses TF-IDF (Term Frequency-Inverse Document Frequency) to convert text to numerical features
- Calculates cosine similarity between products
- Recommends items with highest similarity scores

### 2. User Behavior Analysis
- Tracks user interactions (views, cart additions)
- Stores behavior data in SQLite database
- Analyzes user preferences by category and frequency
- Suggests products from preferred categories that haven't been seen

### 3. Hybrid Approach
- Combines content-based and behavior-based recommendations
- Provides diverse suggestions balancing similarity and personal preferences
- Adapts to user behavior over time

## 📊 Application Structure

```
ecommerce-recommender/
├── app.py                 # Main Streamlit application
├── products.csv           # Product dataset
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── user_behavior.db      # SQLite database (created automatically)
```

## 🎨 Features Breakdown

### Product Search
- Full-text search across names, descriptions, and categories
- Category filtering
- Dynamic results display

### Recommendation Engine
- **Content-Based**: Find similar products using ML
- **User Behavior**: Personalized suggestions based on history
- **Hybrid**: Best of both approaches

### User Dashboard
- Activity tracking and analytics
- Interaction history
- Preference visualization

## 🚀 Deployment on Streamlit Cloud

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set `app.py` as the main file
   - Click "Deploy"

3. **Your app will be live** at `https://your-repo-name.streamlit.app`

## 🔍 Machine Learning Details

### TF-IDF Vectorization
- Converts text descriptions into numerical vectors
- Handles stop words removal
- Uses n-grams (1-2) for better context understanding
- Limited to 5000 features for performance

### Cosine Similarity
- Measures similarity between product vectors
- Range: 0 (completely different) to 1 (identical)
- Efficient computation for real-time recommendations

### User Modeling
- Implicit feedback from interactions
- Category preference learning
- Temporal weighting for recent activities

## 📈 Performance Optimization

- **Caching**: Streamlit's `@st.cache_data` for model and data loading
- **Vectorized Operations**: NumPy and pandas for efficient computation
- **Database Indexing**: Optimized SQLite queries
- **Lazy Loading**: Models built only when needed

## 🎯 Future Enhancements

- [ ] Collaborative filtering using user-user similarity
- [ ] Deep learning models (neural collaborative filtering)
- [ ] A/B testing framework for recommendation algorithms
- [ ] Real-time inventory integration
- [ ] Advanced user segmentation
- [ ] Multi-language support
- [ ] Mobile-responsive design improvements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** for the amazing web app framework
- **scikit-learn** for machine learning tools
- **Unsplash** for product images
- **The open-source community** for inspiration and resources

## 📞 Contact

- **Author**: Your Name
- **Email**: your.email@example.com
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **LinkedIn**: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

⭐ **Star this repository if you found it helpful!**
