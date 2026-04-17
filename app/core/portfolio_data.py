"""Portfolio data - projects and photographs."""

projects = {
    1: {
        "title": "Cyberbullying Detection using Deep Learning",
        "description":
            "A deep learning system to identify derogatory tweets related to gender, race, age, religion, ethnicity, or sexual orientation. Built on a dataset of 110,000 tweets and evaluated using SVM, Random Forest, BERT, and an ensemble of BERT and LSTM models.",
        "tags": [
            "Deep Learning",
            "Natural Language Processing",
            "BERT",
            "LSTM",
            "Text Classification",
            "Social Media Analysis",
            "Python"
        ],
        "link": "https://github.com/Tydos/Cyberbullying-Detection",
        "github": "https://github.com/Tydos/Cyberbullying-Detection",
        "type": "Deep Learning",
        "image":
            "https://raw.githubusercontent.com/Tydos/Cyberbullying-Detection/main/accuracy_comparison.jpg"
    },
    2: {
        "title": "Anuvadak: Indian Sign Language Recognition",
        "description":
            "A deep learning based ISL recognition system using CNN-LSTM architectures. Data was captured via OpenCV, augmented, and processed using MediaPipe Holistic for feature extraction, achieving 85% accuracy. Includes Android deployment.",
        "tags": [
            "Deep Learning",
            "Computer Vision",
            "Gesture Recognition",
            "CNN",
            "LSTM",
            "MediaPipe",
            "OpenCV"
        ],
        "link": "https://github.com/Tydos/ISL",
        "github": "https://github.com/Tydos/ISL",
        "type": "Deep Learning",
        "image":
            "https://res.cloudinary.com/duws62b88/image/upload/v1719502253/ssnop_g67nmy.png"
    },
    3: {
        "title": "Portfolio Website",
        "description":
            "A full-stack MERN portfolio website styled with Tailwind CSS. Features dynamic project rendering from MongoDB and a photography showcase with images served via Cloudinary.",
        "tags": [
            "Full Stack",
            "MERN",
            "React",
            "MongoDB",
            "Tailwind CSS",
            "Cloudinary",
            "Web Design"
        ],
        "link": "https://github.com/Tydos/portfolio",
        "github": "https://github.com/Tydos/portfolio",
        "type": "Web Development",
        "image":
            "https://res.cloudinary.com/duws62b88/image/upload/v1719500501/Screenshot_2024-06-27_203121_atzojq.png"
    },
    4: {
        "title": "Supply Chain Management of Pharmaceutical Drugs",
        "description":
            "A machine learning solution to optimize shipment modes for pharmaceutical drugs. Trained on a 10,000-row supply chain dataset considering expiry dates, shipping costs, and drug types to determine the fastest and most cost-effective delivery method.",
        "tags": [
            "Machine Learning",
            "Optimization",
            "Supply Chain",
            "Predictive Modeling",
            "Data Analysis",
            "Python"
        ],
        "link": "https://github.com/Arnav047/Supply-Chain-Management",
        "github": "https://github.com/Arnav047/Supply-Chain-Management",
        "type": "Machine Learning",
        "image":
            "https://res.cloudinary.com/duws62b88/image/upload/v1719502354/summary_bzpbtl.png"
    },
    5: {
        "title": "DocSpot",
        "description":
            "A document-sharing platform for students using MongoDB and ElasticSearch. PDFs are converted into embeddings using Google Gemini, enabling semantic retrieval. A fine-tuned Google T5 model acts as a chatbot over stored notes.",
        "tags": [
            "Retrieval Augmented Generation",
            "Semantic Search",
            "NLP",
            "ElasticSearch",
            "MongoDB",
            "Chatbot",
            "Embeddings"
        ],
        "link": "https://github.com/Tydos/DocSpot",
        "github": "https://github.com/Tydos/DocSpot",
        "type": "Web Development",
        "image":
            "https://res.cloudinary.com/duws62b88/image/upload/v1719500204/Screenshot_2024-06-05_214207_k8psav.png"
    },
    6: {
        "title": "Guardify: Cyber Security Portal",
        "description":
            "A cyber security portal for managing and reporting cyberbullying complaints. Integrates a machine learning classifier to categorize complaints and stores records in MongoDB for administrative review.",
        "tags": [
            "Cybersecurity",
            "Web Application",
            "Machine Learning",
            "Text Classification",
            "MongoDB",
            "Full Stack"
        ],
        "link": "https://github.com/satts27/HackOverflow-1.0-BitbyBit",
        "github": "https://github.com/satts27/HackOverflow-1.0-BitbyBit",
        "type": "Web Development",
        "image":
            "https://res.cloudinary.com/duws62b88/image/upload/v1719500441/acf91f47-97c8-42ed-b66a-a98844e1a0ad_ki38x1.jpg"
    }
}

photographs = {
    1: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629005/Photographs/DSC08656-01_kgqggd.jpg",
        "title": "Alpine Silence",
        "location": "Swiss Alps",
        "category": "Landscape"
    },
    2: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629006/Photographs/20211126_154906_ge2g9t.jpg",
        "title": "Deep Forest",
        "location": "Oregon, USA",
        "category": "Nature"
    },
    3: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629005/Photographs/DSC00018_q3fjzn.jpg",
        "title": "Golden Hour",
        "location": "Lofoten, Norway",
        "category": "Landscape"
    },
    4: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629006/Photographs/20211124_123051_hclxud.jpg",
        "title": "Orbital View",
        "location": "The Stratosphere",
        "category": "Aero"
    },
    5: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629006/Photographs/DSC00336-01_dkqmq1.jpg",
        "title": "Urban Geometry",
        "location": "Tokyo, Japan",
        "category": "Architecture"
    },
    6: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629006/Photographs/IMG_0083_pm39pe.jpg",
        "title": "Crimson Valley",
        "location": "Utah, USA",
        "category": "Landscape"
    },
    7: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629007/Photographs/HD_20200507_222920_NR-01-01_kqtjpi.jpg",
        "title": "Celestial Paths",
        "location": "Atacama, Chile",
        "category": "Astrophotography"
    },
    8: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629007/Photographs/IMG_0257_jwbwb6.jpg",
        "title": "Monolithic Echo",
        "location": "Iceland",
        "category": "Landscape"
    },
    9: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629007/Photographs/DSC09078-01_c2ixdk.jpg",
        "title": "Silent Corridor",
        "location": "Northern Europe",
        "category": "Minimalism"
    },
    10: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629007/Photographs/IMG_0093_2_w82dy6.jpg",
        "title": "Neon Pulse",
        "location": "Urban Nightscape",
        "category": "Street"
    },
    11: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629008/Photographs/IMG_20190305_215357_yank7x.jpg",
        "title": "Desert Bloom",
        "location": "Western India",
        "category": "Landscape"
    },
    12: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629008/Photographs/IMG_20190214_070326123_yelnrg.jpg",
        "title": "Still Reflections",
        "location": "Coastal India",
        "category": "Travel"
    },
    13: {
        "url": "https://res.cloudinary.com/duws62b88/image/upload/v1686629011/Photographs/LRM_EXPORT_20190121_074405_1_vx3ous.jpg",
        "title": "Morning Transit",
        "location": "South Asia",
        "category": "Street"
    }
}
