"""
ECHO — Candidate Knowledge Profile & Question Generation Engine
Provides tailored technical, project-based, and behavioral questions
with full paired translations in English, Telugu, Hindi, Tamil, and Kannada.
"""

import os
from typing import List, Dict, Any, Optional

BASE_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "py-list-tuple",
        "category": "Python & Backend",
        "role": "python_backend",
        "difficulty": "Foundational",
        "title": "Difference between Lists and Tuples in Python",
        "question": {
            "en": "Explain the difference between Lists and Tuples in Python. When would you use one over the other?",
            "te": "పైథాన్‌లో లిస్ట్‌లు మరియు ట్యుపుల్స్ మధ్య తేడా ఏమిటి? ఒకదానికి బదులు మరొకదాన్ని ఎప్పుడు ఉపయోగిస్తారు?",
            "hi": "पायथन में लिस्ट और टुपल के बीच क्या अंतर है? आप एक के बजाय दूसरे का उपयोग कब करेंगे?",
            "ta": "பைத்தானில் பட்டியல்கள் மற்றும் டூப்பிள்களுக்கு இடையே உள்ள வித்தியாசம் என்ன? ஒன்றை எப்போது மற்றொன்றை விட பயன்படுத்துவீர்கள்?",
            "kn": "ಪೈಥಾನ್‌ನಲ್ಲಿ ಲಿಸ್ಟ್‌ಗಳು ಮತ್ತು ಟುಪಲ್ಸ್‌ಗಳ ನಡುವಿನ ವ್ಯತ್ಯಾಸವೇನು? ಒಂದರ ಬದಲಿಗೆ ಇನ್ನೊಂದನ್ನು ಯಾವಾಗ ಬಳಸುತ್ತೀರಿ?"
        },
        "expected_concepts": [
            "mutability vs immutability",
            "syntax [] vs ()",
            "memory overhead and performance",
            "hashability and dictionary keys",
            "data integrity for fixed constants"
        ],
        "sample_answers": {
            "te": {
                "text": "పైథాన్‌లో లిస్ట్ అంటే మ్యూటబుల్ కలెక్షన్, అంటే మనం ఎలిమెంట్స్ ని చేంజ్ చేయొచ్చు, అపెండ్ చేయొచ్చు, రిమూవ్ చేయొచ్చు. స్క్వేర్ బ్రాకెట్స్ వాడతాము. ట్యుపుల్ అంటే ఇమ్మ్యూటబుల్, అంటే ఒక్కసారి క్రియేట్ చేశాక చేంజ్ చేయలేము, పేరెంథిసిస్ వాడతాము. ట్యుపుల్స్ మెమరీ తక్కువ తీసుకుంటాయి, ఇంకా డిక్షనరీ కీస్ గా కూడా వాడొచ్చు ఎందుకంటే అవి హ్యాషబుల్.",
                "concept_score": 9.5
            },
            "hi": {
                "text": "पायथन में लिस्ट म्यूटेबल होती है, यानी हम डेटा को बाद में बदल सकते हैं, अपेंड या डिलीट कर सकते हैं। इसके लिए स्क्वायर ब्रैकेट्स इस्तेमाल होते हैं। टुपल इम्यूटेबल होता है, एक बार बनाने के बाद चेंज नहीं किया जा सकता। टुपल्स मेमोरी में तेज़ होते हैं और इन्हें डिक्शनरी की के रूप में भी यूज़ किया जा सकता है।",
                "concept_score": 9.2
            },
            "ta": {
                "text": "பைத்தானில் பட்டியல் (List) என்பது மாற்றக்கூடியது (mutable), நாம் கூறுகளை மாற்றலாம். ஆனால் டூப்பிள் (Tuple) என்பது மாற்ற முடியாதது (immutable). டூப்பிள் குறைந்த நினைவகத்தைப் பயன்படுத்துகிறது மேலும் அகராதி சாவிகளாகப் (dictionary keys) பயன்படுத்தலாம்.",
                "concept_score": 9.0
            },
            "kn": {
                "text": "ಪೈಥಾನ್‌ನಲ್ಲಿ ಲಿಸ್ಟ್ ಮ್ಯೂಟೇಬಲ್ ಆಗಿರುತ್ತದೆ, ನಾವು ಡೇಟಾ ಬದಲಾಯಿಸಬಹುದು. ಟುಪಲ್ ಇಮ್ಮ್ಯೂಟೇಬಲ್ ಆಗಿರುತ್ತದೆ. ಟುಪಲ್‌ಗಳು ಕಡಿಮೆ ಮೆಮೊರಿ ಬಳಸುತ್ತವೆ ಮತ್ತು ಡಿಕ್ಷನರಿ ಕೀಗಳಾಗಿ ಬಳಸಬಹುದು.",
                "concept_score": 9.0
            },
            "en_hesitant": {
                "text": "Uh, list in Python is with square brackets, and we can change values. Tuple is round bracket, and cannot change. Tuple is fast, I think.",
                "fluency_score": 5.5
            },
            "en_golden": {
                "text": "In Python, the primary distinction is mutability: lists are mutable and enclosed in square brackets, allowing runtime additions and modifications, whereas tuples are immutable and defined using parentheses. Because tuples are immutable, they have a smaller memory footprint, execute slightly faster, and are hashable, making them suitable as dictionary keys or for fixed data integrity.",
                "fluency_score": 9.8
            }
        }
    },
    {
        "id": "web-virtual-dom",
        "category": "Frontend & React",
        "role": "frontend_react",
        "difficulty": "Intermediate",
        "title": "Virtual DOM and Reconciliation Process",
        "question": {
            "en": "What is the Virtual DOM in React, and how does the reconciliation process optimize UI rendering?",
            "te": "రియాక్ట్‌లో వర్చువల్ డామ్ (Virtual DOM) అంటే ఏమిటి? రీకాన్సిలియేషన్ ప్రాసెస్ ద్వారా యూఐ రెండరింగ్ ఎలా ఆప్టిమైజ్ అవుతుంది?",
            "hi": "रिएक्ट में वर्चुअल DOM क्या है, और रीकॉन्सिलिएशन प्रक्रिया UI रेंडरिंग को कैसे ऑप्टिमाइज़ करती है?",
            "ta": "ரியாக்டில் விர்ச்சுவல் DOM என்றால் என்ன, மற்றும் ரீகான்சிலியேஷன் செயல்முறை UI ரெண்டரிங்கை எவ்வாறு மேம்படுத்துகிறது?",
            "kn": "ರಿಯಾಕ್ಟ್‌ನಲ್ಲಿ ವರ್ಚುವಲ್ DOM ಎಂದರೇನು ಮತ್ತು ರೀಕಾನ್ಸಿಲಿಯೇಶನ್ ಪ್ರಕ್ರಿಯೆಯು UI ರೆಂಡರಿಂಗ್ ಅನ್ನು ಹೇಗೆ ಆಪ್ಟಿಮೈಸ್ ಮಾಡುತ್ತದೆ?"
        },
        "expected_concepts": [
            "in-memory representation of real DOM",
            "diffing algorithm and tree comparison",
            "batched updates to real DOM",
            "minimizing expensive browser reflows and repaints",
            "keys in lists for component identity"
        ],
        "sample_answers": {
            "te": {
                "text": "రియాక్ట్ లో వర్చువల్ డామ్ అనేది రియల్ బ్రౌజర్ డామ్ కి ఒక లైట్ వెయిట్ జావాస్క్రిప్ట్ ఆబ్జెక్ట్ కాపీ. ఏదైనా స్టేట్ చేంజ్ అయినప్పుడు, రియాక్ట్ కొత్త వర్చువల్ డామ్ ట్రీ ని క్రియేట్ చేస్తుంది. పాత ట్రీ తో కొత్త ట్రీ ని డిఫింగ్ అల్గోరిథం ద్వారా కంపేర్ చేసి, కేవలం మారిన ఎలిమెంట్స్ ని మాత్రమే రియల్ డామ్ లో అప్‌డేట్ చేస్తుంది.",
                "concept_score": 9.7
            },
            "hi": {
                "text": "वर्चुअल DOM रिएक्ट में रियल DOM का एक जावास्क्रिप्ट रिप्रेजेंटेशन है। जब भी कोई स्टेट बदलती है, तो रिएक्ट नया वर्चुअल DOM बनाकर पुराने से तुलना (Diffing) करता है और सिर्फ बदले हुए भाग को रियल DOM में बैच करके अपडेट करता है।",
                "concept_score": 9.3
            },
            "ta": {
                "text": "விர்ச்சுவல் DOM என்பது உண்மையான DOM இன் நினைவக நகலாகும். நிலை (state) மாறும்போது, டிஃப்பிங் (diffing) அல்காரிதம் மூலம் மாற்றங்களை மட்டும் அடையாளம் கண்டு உண்மையான DOM ஐப் புதுப்பிக்கிறது.",
                "concept_score": 9.1
            },
            "kn": {
                "text": "ವರ್ಚುವಲ್ DOM ಎಂಬುದು ನೈಜ DOM ನ ಜಾವಾಸ್ಕ್ರಿಪ್ಟ್ ಆಬ್ಜೆಕ್ಟ್ ನಕಲು. ಸ್ಟೇಟ್ ಬದಲಾದಾಗ, ಡಿಫಿಂಗ್ ಅಲ್ಗಾರಿದಮ್ ಮೂಲಕ ಕೇವಲ ಬದಲಾದ ಭಾಗವನ್ನು ಮಾತ್ರ ಅಪ್ಡೇಟ್ ಮಾಡುತ್ತದೆ.",
                "concept_score": 9.0
            },
            "en_hesitant": {
                "text": "Virtual DOM is like duplicate of DOM in JS. When click button, it compares and changes only that place. Real DOM is very slow, so virtual DOM is fast.",
                "fluency_score": 5.8
            },
            "en_golden": {
                "text": "The Virtual DOM is a lightweight in-memory representation of the actual browser DOM. When component state updates occur, React generates a new Virtual DOM tree and runs a diffing algorithm (Reconciliation) against the previous tree. It computes the minimal set of changes and batches updates to the real DOM, preventing costly browser reflows and repaints.",
                "fluency_score": 9.7
            }
        }
    },
    {
        "id": "dsa-hashmap-collisions",
        "category": "Data Structures & Algorithms",
        "role": "dsa_sde",
        "difficulty": "Intermediate",
        "title": "Hash Table Collisions and Resolution Techniques",
        "question": {
            "en": "What is a collision in a Hash Table, and how do separate chaining and open addressing resolve it?",
            "te": "హాష్ టేబుల్‌లో కొలిజన్ (Collision) అంటే ఏమిటి? సెపరేట్ చైనింగ్ మరియు ఓపెన్ అడ్రెస్సింగ్ పద్ధతులు దీనిని ఎలా పరిష్కరిస్తాయి?",
            "hi": "हैश टेबल में कोलिजन क्या है, और सेपरेट चेनिंग और ओपन एड्रेसिंग इसे कैसे हल करते हैं?",
            "ta": "ஹாஷ் அட்டவணையில் மோதல் (Collision) என்றால் என்ன, அதைத் தீர்க்கும் முறைகள் யாவை?",
            "kn": "ಹ್ಯಾಶ್ ಟೇಬಲ್‌ನಲ್ಲಿ ಘರ್ಷಣೆ (Collision) ಎಂದರೇನು, ಮತ್ತು ಅದನ್ನು ಹೇಗೆ ಪರಿಹರಿಸಲಾಗುತ್ತದೆ?"
        },
        "expected_concepts": [
            "hash function mapping two keys to the same bucket index",
            "separate chaining with linked lists or balanced trees",
            "open addressing with linear probing, quadratic probing, or double hashing",
            "load factor threshold and dynamic rehashing",
            "average O(1) versus worst-case O(n) lookup tradeoffs"
        ],
        "sample_answers": {
            "te": {
                "text": "హాష్ టేబుల్ లో రెండు వేర్వేరు కీస్ కి హాష్ ఫంక్షన్ ఒకే ఇండెక్స్ కాలిక్యులేట్ చేసినప్పుడు కొలిజన్ జరుగుతుంది. దీన్ని సాల్వ్ చేయడానికి రెండు మెయిన్ పద్ధతులు ఉన్నాయి. ఒకటి సెపరేట్ చైనింగ్ - ఇందులో ప్రతి బకెట్ లో లింక్డ్ లిస్ట్ పెడతాము. రెండవది ఓపెన్ అడ్రెస్సింగ్ - ఇందులో నెక్స్ట్ ఖాళీ స్లాట్ కోసం లీనియర్ లేదా క్వాడ్రాటిక్ ప్రోబింగ్ వాడతాము.",
                "concept_score": 9.6
            },
            "hi": {
                "text": "जब हैश फंक्शन दो अलग-अलग कीज़ के लिए एक ही इंडेक्स देता है, तो उसे कोलिजन कहते हैं। इसे हल करने के लिए सेपरेट चेनिंग में हर स्लॉट पर लिंक्ड लिस्ट बनाते हैं, और ओपन एड्रेसिंग में प्रोबिंग के ज़रिए खाली स्लॉट ढूंढते हैं।",
                "concept_score": 9.3
            },
            "ta": {
                "text": "இரண்டு வெவ்வேறு சாவிகள் ஒரே அட்டவணை குறியீட்டை (index) உருவாக்கும் போது மோதல் ஏற்படுகிறது. தனி இணைப்பு (Separate chaining) மற்றும் திறந்த முகவரியிடல் (Open addressing) மூலம் இதை சரிசெய்யலாம்.",
                "concept_score": 9.0
            },
            "kn": {
                "text": "ಎರಡು ಕೀಗಳು ಒಂದೇ ಹ್ಯಾಶ್ ಇಂಡೆಕ್ಸ್ ಪಡೆದಾಗ ಘರ್ಷಣೆ ಉಂಟಾಗುತ್ತದೆ. ಚೈನಿಂಗ್ ಮತ್ತು ಓಪನ್ ಅಡ್ರೆಸ್ಸಿಂಗ್ ವಿಧಾನಗಳಿಂದ ಇದನ್ನು ಪರಿಹರಿಸಬಹುದು.",
                "concept_score": 9.0
            },
            "en_hesitant": {
                "text": "Collision means two items want same box in table. To fix, we can make a list inside the box, or we look for next empty box. If full, we resize.",
                "fluency_score": 5.4
            },
            "en_golden": {
                "text": "A collision occurs when a hash function maps two distinct keys to the same index in the underlying array. In Separate Chaining, each bucket stores a pointer to a data structure like a linked list or balanced tree to hold multiple entries. In Open Addressing, collisions are resolved by probing for alternative vacant slots using techniques like linear probing, quadratic probing, or double hashing. When the load factor exceeds a threshold, the table rehashes into a larger capacity.",
                "fluency_score": 9.9
            }
        }
    },
    {
        "id": "ds-overfitting",
        "category": "AI & Data Science",
        "role": "ai_ml",
        "difficulty": "Intermediate",
        "title": "Overfitting vs Underfitting and Regularization",
        "question": {
            "en": "What is overfitting in machine learning, and what techniques do you use to detect and prevent it?",
            "te": "మెషిన్ లెర్నింగ్‌లో ఓవర్‌ఫిట్టింగ్ అంటే ఏమిటి? దానిని గుర్తించడానికి మరియు నివారించడానికి మీరు ఏ పద్ధతులను ఉపయోగిస్తారు?",
            "hi": "मशीन लर्निंग में ओवरफिटिंग क्या है, और आप इसका पता लगाने और इसे रोकने के लिए किन तकनीकों का उपयोग करते हैं?",
            "ta": "மெஷின் லேர்னிங்கில் ஓவர்ஃபிட்டிங் என்றால் என்ன, அதை எவ்வாறு தடுத்து சரிசெய்வது?",
            "kn": "ಮೆಷಿನ್ ಲರ್ನಿಂಗ್‌ನಲ್ಲಿ ಓವರ್‌ಫಿಟ್ಟಿಂಗ್ ಎಂದರೇನು, ಮತ್ತು ಅದನ್ನು ತಡೆಗಟ್ಟಲು ನೀವು ಯಾವ ತಂತ್ರಗಳನ್ನು ಬಳಸುತ್ತೀರಿ?"
        },
        "expected_concepts": [
            "high variance and low bias",
            "model memorizing training noise instead of general patterns",
            "training error low versus validation error high",
            "regularization methods (L1 Lasso, L2 Ridge, Dropout)",
            "cross-validation, early stopping, and data augmentation"
        ],
        "sample_answers": {
            "te": {
                "text": "ఓవర్‌ఫిట్టింగ్ అంటే మోడల్ ట్రైనింగ్ డేటాలోని నాయిస్‌ని కూడా నేర్చుకుని మెమోరైజ్ చేసుకోవడం. దీనివల్ల ట్రైనింగ్ అక్యూరసీ చాలా ఎక్కువగా ఉంటుంది కానీ టెస్ట్ లేదా వ్యాలిడేషన్ డేటాపై పర్ఫార్మెన్స్ పడిపోతుంది. దీన్ని ప్రివెంట్ చేయడానికి L1, L2 రెగ్యులరైజేషన్, న్యూరల్ నెట్‌వర్క్స్‌లో డ్రాపౌట్, క్రాస్-వ్యాలిడేషన్, ఎర్లీ స్టాపింగ్ వాడతాం.",
                "concept_score": 9.7
            },
            "hi": {
                "text": "ओवरफिटिंग तब होती है जब मॉडल ट्रेनिंग डेटा को याद कर लेता है और नए डेटा पर खराब परफॉर्म करता है। इसे रोकने के लिए L1/L2 रेगुलराइजेशन, ड्रॉपआउट, क्रॉस-वैलिडेशन और अर्ली स्टॉपिंग का इस्तेमाल किया जाता है।",
                "concept_score": 9.2
            },
            "ta": {
                "text": "ஓவர்ஃபிட்டிங் என்பது மாடல் பயிற்சித் தரவை அதிகமாக மனப்பாடம் செய்து புதிய தரவில் தோல்வியடைவதாகும். இதைத் தடுக்க எல்1, எல்2 முறைப்படுத்தல் மற்றும் ஆரம்பத்திலேயே நிறுத்துதல் (early stopping) உதவும்.",
                "concept_score": 8.9
            },
            "kn": {
                "text": "ಮಾಡೆಲ್ ತರಬೇತಿ ಡೇಟಾದ ನಾಯ್ಸ್ ಅನ್ನು ಮೆಮೊರೈಸ್ ಮಾಡಿಕೊಂಡಾಗ ಓವರ್‌ಫಿಟ್ಟಿಂಗ್ ಆಗುತ್ತದೆ. L1/L2 ರೆಗ್ಯುಲರೈಸೇಶನ್ ಮತ್ತು ಡ್ರಾಪ್‌ಔಟ್ ಮೂಲಕ ಇದನ್ನು ತಡೆಗಟ್ಟಬಹುದು.",
                "concept_score": 8.9
            },
            "en_hesitant": {
                "text": "Overfitting is model is too good in training, but fail in testing. It memorizes noise. We can stop early, make data bigger, or use dropout in neural network.",
                "fluency_score": 6.2
            },
            "en_golden": {
                "text": "Overfitting occurs when a model exhibits high variance by learning the noise and idiosyncrasies of the training data rather than underlying generalizable patterns, resulting in low training error but high validation error. We diagnose it using learning curves and cross-validation, and mitigate it using L1/L2 regularization penalties, dropout in deep architectures, early stopping, pruning, and data augmentation.",
                "fluency_score": 9.8
            }
        }
    },
    {
        "id": "hr-difficult-bug",
        "category": "HR & Behavioral",
        "role": "hr_behavioral",
        "difficulty": "Foundational",
        "title": "Explain a Challenging Bug or Technical Obstacle You Solved",
        "question": {
            "en": "Describe a challenging technical bug or problem you recently encountered. How did you diagnose and resolve it?",
            "te": "మీరు ఇటీవల ఎదుర్కొన్న ఒక క్లిష్టమైన టెక్నికల్ బగ్ లేదా సమస్యను వివరించండి. మీరు దానిని ఎలా విశ్లేషించి పరిష్కరించారు?",
            "hi": "हाल ही में आपके द्वारा हल किए गए किसी कठिन तकनीकी बग का वर्णन करें। आपने उसका विश्लेषण और समाधान कैसे किया?",
            "ta": "நீங்கள் சமீபத்தில் எதிர்கொண்ட கடினமான தொழில்நுட்ப சிக்கலை விவரிக்கவும். அதை எவ்வாறு சரிசெய்தீர்கள்?",
            "kn": "ನೀವು ಇತ್ತೀಚೆಗೆ ಪರಿಹರಿಸಿದ ಕಠಿಣ ತಾಂತ್ರಿಕ ದೋಷ ಅಥವಾ ಸಮಸ್ಯೆಯನ್ನು ವಿವರಿಸಿ. ಅದನ್ನು ನೀವು ಹೇಗೆ ಪತ್ತೆಹಚ್ಚಿ ಪರಿಹರಿಸಿದ್ದೀರಿ?"
        },
        "expected_concepts": [
            "STAR method (Situation, Task, Action, Result)",
            "systematic debugging and root cause profiling",
            "communication and collaborative resolution",
            "prevention through tests, alerts, and defensive code"
        ],
        "sample_answers": {
            "te": {
                "text": "మా ప్రాజెక్ట్ ప్రొడక్షన్ లో ఒక మెమరీ లీక్ బగ్ వచ్చింది, సర్వర్ ప్రతి 3 రోజులకు క్రాష్ అయ్యేది. నేను నోడ్.జెఎస్ హీప్ స్నాప్‌షాట్స్ తీసుకుని ప్రొఫైల్ చేసాను. అప్పుడు తెలిసింది అన్‌క్లోజ్డ్ డేటాబేస్ కనెక్షన్ పూల్స్ మెమరీ ని హోల్డ్ చేస్తున్నాయని. నేను కనెక్షన్ క్లీనప్ మిడిల్‌వేర్ రాసి, టెస్ట్స్ యాడ్ చేసాను. ఆ తర్వాత మెమరీ యూసేజ్ 65% తగ్గింది.",
                "concept_score": 9.5
            },
            "hi": {
                "text": "हमारे प्रोडक्शन सर्वर में मेमोरी लीक था जिससे सर्वर क्रैश हो रहा था। मैंने हीप डंप्स का विश्लेषण किया और पाया कि अनक्लोज्ड डीबी कनेक्शंस जिम्मेदार थे। मैंने कनेक्शन पूल फिक्स किया और ऑटोमेटेड टेस्ट्स जोड़े जिससे 65% मेमोरी घटी।",
                "concept_score": 9.1
            },
            "ta": {
                "text": "எங்கள் தயாரிப்பில் நினைவகக் கசிவு (memory leak) இருந்தது. நான் ஹீப் டம்ப்களை ஆய்வு செய்து தரவுத்தள இணைப்பு சிக்கலைக் கண்டறிந்து சரிசெய்தேன். 65% நினைவகப் பயன்பாடு குறைந்தது.",
                "concept_score": 9.0
            },
            "kn": {
                "text": "ನಮ್ಮ ಸರ್ವರ್‌ನಲ್ಲಿ ಮೆಮೊರಿ ಲೀಕ್ ಸಮಸ್ಯೆ ಇತ್ತು. ನಾನು ಹೀಪ್ ಡಂಪ್ ಪ್ರೊಫೈಲ್ ಮಾಡಿ ಡಾಟಾಬೇಸ್ ಕನೆಕ್ಷನ್ ಲೀಕ್ ಸರಿಪಡಿಸಿದೆ, ಇದರಿಂದ ಮೆಮೊರಿ ಬಳಕೆ 65% ಕಡಿಮೆಯಾಯಿತು.",
                "concept_score": 9.0
            },
            "en_hesitant": {
                "text": "In my project server crashed because memory problem. I saw heap dump and found database connection was not closed properly. I fixed the code and added tests. Then server worked fine.",
                "fluency_score": 6.0
            },
            "en_golden": {
                "text": "In our production environment, we observed progressive memory bloat causing service restarts every 72 hours. I took diagnostic heap snapshots and profiled allocations, identifying uncollected database connection listeners in an asynchronous middleware pipeline. I refactored the connection lifecycle management, implemented automated leak regression tests, and set up Prometheus alert thresholds, which reduced steady-state memory consumption by 65%.",
                "fluency_score": 9.8
            }
        }
    },
    {   'category': 'Database Architecture',
    'difficulty': 'Intermediate',
    'expected_concepts': [   'balanced search tree',
                             'O(log n) lookup vs O(n) table scan',
                             'write amplification on insert/update',
                             'composite index column order',
                             'clustered vs non-clustered index'],
    'id': 'sys-db-indexing',
    'question': {   'en': 'How do database indexes like B-Trees work under the hood, and how do they balance query '
                          'read speed against write overhead?',
                    'hi': 'डेटाबेस इंडेक्स (B-Tree) अंदरूनी तौर पर कैसे काम करते हैं, और वे रीड स्पीड और राइट ओवरहेड '
                          'को कैसे संतुलित करते हैं?',
                    'kn': 'ಡೇಟಾಬೇಸ್ ಇಂಡೆಕ್ಸ್\u200cಗಳು (B-Trees) ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತವೆ ಮತ್ತು ಅವು ರೀಡ್ ವೇಗ ಮತ್ತು ರೈಟ್ '
                          'ಓವರ್\u200cಹೆಡ್ ನಡುವೆ ಹೇಗೆ ಸಮತೋಲನ ಸಾಧಿಸುತ್ತವೆ?',
                    'ta': 'தரவுத்தள குறியீடுகள் (B-Trees) எவ்வாறு செயல்படுகின்றன, மேலும் அவை வாசிப்பு வேகம் மற்றும் '
                          'எழுதும் சுமையை எவ்வாறு சமநிலைப்படுத்துகின்றன?',
                    'te': 'డేటాబేస్ ఇండెక్సెస్ (B-Trees) అంతర్గతంగా ఎలా పనిచేస్తాయి? అవి క్వెరీ రీడ్ స్పీడ్ మరియు రైట్ '
                          'ఓవర్\u200cహెడ్ మధ్య సమతుల్యతను ఎలా సాధిస్తాయి?'},
    'role': 'backend_database',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.8,
                                           'text': 'Database B-Tree indexes maintain a balanced multi-level tree of '
                                                   'sorted keys and row pointers, reducing search complexity from an '
                                                   'O(N) full table scan to O(log N) block traversals. However, every '
                                                   'write, update, or delete operation incurs a maintenance cost '
                                                   'because the engine must rebalance nodes and split pages, making '
                                                   'index design a careful tradeoff between query latency and write '
                                                   'throughput.'},
                          'te': {   'concept_score': 9.6,
                                    'text': 'డేటాబేస్ ఇండెక్స్ అనేది బ్యాలెన్స్\u200cడ్ బి-ట్రీ స్ట్రక్చర్. ఇది O(N) '
                                            'ఫుల్ టేబుల్ స్కాన్ ని O(log N) సెర్చ్\u200cగా తగ్గిస్తుంది. అయితే ప్రతి '
                                            'ఇన్సర్ట్ లేదా అప్\u200cడేట్ లో ట్రీ రీబ్యాలెన్సింగ్ జరగడం వల్ల రైట్ '
                                            'పెర్ఫార్మెన్స్ కాస్త తగ్గుతుంది.'}},
    'title': 'Database B-Tree Indexing & Performance Tradeoffs'},
    {   'category': 'API & Microservices',
    'difficulty': 'Advanced',
    'expected_concepts': [   'HTTP/2 multiplexing vs HTTP/1.1',
                             'Protocol Buffers binary serialization vs JSON text',
                             'contract-first proto schema',
                             'bidirectional streaming',
                             'low latency inter-service RPC'],
    'id': 'api-rest-grpc',
    'question': {   'en': 'Compare REST, gRPC, and GraphQL for microservice communication. When would you choose gRPC '
                          'over REST?',
                    'hi': 'माइक्रोसर्विस संचार के लिए REST, gRPC और GraphQL की तुलना करें। आप REST की तुलना में gRPC '
                          'कब चुनेंगे?',
                    'kn': 'ಮೈಕ್ರೋಸರ್ವಿಸ್ ಸಂವಹನಕ್ಕಾಗಿ REST, gRPC ಮತ್ತು GraphQL ಅನ್ನು ಹೋಲಿಸಿ. REST ಗಿಂತ gRPC ಅನ್ನು ಯಾವಾಗ '
                          'ಆರಿಸಿಕೊಳ್ಳುತ್ತೀರಿ?',
                    'ta': 'மைக்ரோ சர்வீஸ் தொடர்புக்கு REST, gRPC மற்றும் GraphQL ஐ ஒப்பிடுக. REST ஐ விட gRPC ஐ எப்போது '
                          'தேர்ந்தெடுப்பீர்கள்?',
                    'te': 'మైక్రోసర్వీసెస్ కమ్యూనికేషన్ కోసం REST, gRPC మరియు GraphQL లను సరిపోల్చండి. REST కంటే gRPC '
                          'ని ఎప్పుడు ఎంచుకుంటారు?'},
    'role': 'backend_api',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.9,
                                           'text': 'While REST operates on resource-oriented JSON over HTTP/1.1, gRPC '
                                                   'leverages binary Protocol Buffers over HTTP/2 with persistent '
                                                   'multiplexed TCP streams and bidirectional streaming. gRPC is '
                                                   'vastly superior for high-throughput internal '
                                                   'microservice-to-microservice communication where ultra-low latency '
                                                   'and strict contract validation are paramount, whereas REST remains '
                                                   'ideal for public customer-facing APIs.'},
                          'te': {   'concept_score': 9.7,
                                    'text': 'REST సాధారణంగా హెచ్\u200cటిటిపి 1.1 మరియు జేసన్ వాడుతుంది. gRPC '
                                            'హెచ్\u200cటిటిపి 2 మరియు ప్రోటోకాల్ బఫర్స్ వాడటం వల్ల సైజ్ చాలా తక్కువగా '
                                            'ఉంటుంది మరియు స్ట్రీమింగ్ సపోర్ట్ చేస్తుంది. ఇంటర్నల్ మైక్రోసర్వీస్ '
                                            'కమ్యూనికేషన్ లో హై త్రూపుట్ కోసం gRPC ని ఎంచుకుంటాము.'}},
    'title': 'REST vs gRPC & GraphQL in Microservice Architectures'},
    {   'category': 'Cloud & Containers',
    'difficulty': 'Intermediate',
    'expected_concepts': [   'shared host OS kernel vs guest OS hypervisor',
                             'cgroups and namespaces isolation',
                             'ephemeral lightweight startup',
                             'multi-stage build separating compiler artifacts from runtime',
                             'minimal base image like Alpine or distroless'],
    'id': 'devops-docker-vm',
    'question': {   'en': 'What is the architectural difference between Docker containers and Virtual Machines, and '
                          'how do multi-stage Docker builds optimize image size?',
                    'hi': 'डॉकर कंटेनर और वर्चुअल मशीन के बीच क्या तकनीकी अंतर है, और मल्टी-स्टेज बिल्ड इमेज साइज़ को '
                          'कैसे कम करते हैं?',
                    'kn': 'ಡಾಕರ್ ಕಂಟೈನರ್\u200cಗಳು ಮತ್ತು ವರ್ಚುವಲ್ ಮೆಷಿನ್\u200cಗಳ ನಡುವಿನ ವಾಸ್ತುಶಿಲ್ಪ ವ್ಯತ್ಯಾಸವೇನು? '
                          'ಮಲ್ಟಿ-ಸ್ಟೇಜ್ ಬಿಲ್ಡ್ ಇಮೇಜ್ ಗಾತ್ರವನ್ನು ಹೇಗೆ ಆಪ್ಟಿಮೈಸ್ ಮಾಡುತ್ತದೆ?',
                    'ta': 'டாக்கர் கொள்கலன்கள் மற்றும் விர்ச்சுவல் மெஷின்களுக்கு இடையே உள்ள கட்டமைப்பு வேறுபாடு என்ன? '
                          'மல்டி-ஸ்டேஜ் பில்ட் எவ்வாறு இமேஜ் அளவை மேம்படுத்துகிறது?',
                    'te': 'డాకర్ కంటైనర్లు మరియు వర్చువల్ మెషీన్ల మధ్య ఆర్కిటెక్చరల్ తేడా ఏమిటి? మల్టీ-స్టేజ్ బిల్డ్స్ '
                          'డాకర్ ఇమేజ్ సైజును ఎలా తగ్గిస్తాయి?'},
    'role': 'devops_cloud',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.8,
                                           'text': 'Virtual Machines virtualize hardware layers via a hypervisor where '
                                                   'each instance runs a full guest OS. Docker containers share the '
                                                   'host Linux kernel, using namespaces and cgroups for process '
                                                   'isolation, resulting in sub-second boot times. Multi-stage builds '
                                                   'compile artifacts in a builder image and copy only production '
                                                   'binaries into a stripped runtime container like Alpine, '
                                                   'drastically minimizing footprint and attack surface.'},
                          'te': {   'concept_score': 9.6,
                                    'text': 'విఎంలు హైపర్\u200cవైజర్ ద్వారా ప్రతి ఓఎస్\u200cని సపరేట్\u200cగా రన్ '
                                            'చేస్తాయి. డాకర్ హోస్ట్ కర్నల్\u200cని షేర్ చేసుకుంటూ నేమ్\u200cస్పేసెస్ '
                                            'ద్వారా ప్రాసెస్ ఐసోలేషన్ ఇస్తుంది. మల్టీ-స్టేజ్ బిల్డ్\u200cలో కోడ్ '
                                            'కంపైల్ చేసే టూల్స్ ని తీసివేసి కేవలం రన్\u200cటైమ్ ఫైల్స్ మాత్రమే ఫైనల్ '
                                            'ఇమేజ్\u200cలో ఉంచుతాము.'}},
    'title': 'Docker Containers vs Virtual Machines & Multi-stage Builds'},
    {   'category': 'Distributed Systems',
    'difficulty': 'Advanced',
    'expected_concepts': [   'Atomicity, Consistency, Isolation, Durability',
                             'Consistency, Availability, Partition Tolerance',
                             'network partitions forcing trade-off between C and A',
                             'eventual consistency and BASE model',
                             'two-phase commit vs saga pattern'],
    'id': 'db-acid-cap',
    'question': {   'en': 'Explain the ACID properties in relational databases and how the CAP theorem influences '
                          'choices in distributed database architectures.',
                    'hi': 'रिलेशनल डेटाबेस में ACID गुण क्या हैं और CAP प्रमेय वितरित डेटाबेस सिस्टम में निर्णयों को '
                          'कैसे प्रभावित करता है?',
                    'kn': 'ರಿಲೇಶನಲ್ ಡೇಟಾಬೇಸ್\u200cನಲ್ಲಿ ACID ಗುಣಲಕ್ಷಣಗಳು ಎಂದರೇನು ಮತ್ತು CAP ಪ್ರಮೇಯವು ವಿತರಿಸಿದ '
                          'ಡೇಟಾಬೇಸ್\u200cಗಳಲ್ಲಿ ಆಯ್ಕೆಗಳನ್ನು ಹೇಗೆ ಪ್ರಭಾವಿಸುತ್ತದೆ?',
                    'ta': 'ACID பண்புகள் என்றால் என்ன, மற்றும் விநியோகிக்கப்பட்ட தரவுத்தளங்களில் CAP தேற்றம் எவ்வாறு '
                          'தேர்வுகளை பாதிக்கிறது?',
                    'te': 'రిలేషనల్ డేటాబేస్\u200cలలో ACID లక్షణాలు ఏమిటి? డిస్ట్రిబ్యూటెడ్ ఆర్కిటెక్చర్\u200cలలో CAP '
                          'సిద్ధాంతం నిర్ణయాలను ఎలా ప్రభావితం చేస్తుంది?'},
    'role': 'system_design',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.9,
                                           'text': 'ACID guarantees that transactions are Atomic, maintain schema '
                                                   'Constraints, execute in Isolation without race conditions, and '
                                                   'remain Durable across crashes. In distributed systems, the CAP '
                                                   'theorem proves that under inevitable network partitions, a system '
                                                   'cannot simultaneously guarantee both immediate Consistency and '
                                                   'continuous Availability. Teams must choose between CP systems like '
                                                   'CockroachDB or AP architectures like Cassandra with eventual '
                                                   'consistency.'},
                          'te': {   'concept_score': 9.7,
                                    'text': 'యాసిడ్ (ACID) అంటే ట్రాన్సాక్షన్ పూర్తిగా జరగడం (Atomicity), నిబంధనలు '
                                            'పాటించడం (Consistency), ఐసోలేషన్ మరియు పర్మనెంట్ గా స్టోర్ అవ్వడం '
                                            '(Durability). CAP థియరమ్ ప్రకారం నెట్\u200cవర్క్ పార్టిషన్ వచ్చినప్పుడు '
                                            'Consistency లేదా Availability లో ఒకదాన్ని మాత్రమే ఎంచుకోగలము.'}},
    'title': 'ACID Guarantees and the CAP Theorem Tradeoffs'},
    {   'category': 'System Design & Caching',
    'difficulty': 'Advanced',
    'expected_concepts': [   'Cache-Aside lazy loading',
                             'Write-Through synchronous dual write',
                             'Write-Behind asynchronous batch update',
                             'Cache Stampede when key expires under high concurrency',
                             'distributed mutex locking and probabilistic early expiration'],
    'id': 'sys-caching-strategies',
    'question': {   'en': 'Compare Cache-Aside, Write-Through, and Write-Behind caching strategies. How do you prevent '
                          'cache stampede (thundering herd) under heavy traffic?',
                    'hi': 'कैश-असाइड, राइट-थ्रू और राइट-बिहाइंड कैशिंग रणनीतियों की तुलना करें। भारी ट्रैफ़िक में कैश '
                          'स्टैम्पेड को कैसे रोकते हैं?',
                    'kn': 'ಕ್ಯಾಶಿಂಗ್ ತಂತ್ರಗಳನ್ನು ಹೋಲಿಕೆ ಮಾಡಿ. ಹೆಚ್ಚಿನ ಟ್ರಾಫಿಕ್ ಇದ್ದಾಗ ಕ್ಯಾಶ್ ಸ್ಟ್ಯಾಂಪೀಡ್ (thundering '
                          'herd) ಅನ್ನು ಹೇಗೆ ತಡೆಯುತ್ತೀರಿ?',
                    'ta': 'கேச்சிங் உத்திகளை (Cache-Aside, Write-Through, Write-Behind) ஒப்பிடுக. அதிக போக்குவரத்தின் '
                          'போது கேச் ஸ்டாம்பீட் சிக்கலை எவ்வாறு தடுப்பீர்கள்?',
                    'te': 'క్యాష్-అసైడ్, రైట్-త్రూ మరియు రైట్-బిహైండ్ క్యాషింగ్ పద్ధతులను సరిపోల్చండి. అధిక ట్రాఫిక్ '
                          'ఉన్నప్పుడు క్యాష్ స్టాంపేడ్ (Thundering Herd) ను ఎలా నిరోధిస్తారు?'},
    'role': 'backend_architecture',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.9,
                                           'text': 'Under Cache-Aside, the application queries the cache first and '
                                                   'populates it lazily on miss; Write-Through updates cache and '
                                                   'database synchronously; Write-Behind buffers updates in memory and '
                                                   'writes asynchronously in batches. To prevent a cache stampede when '
                                                   'a hot key expires, we utilize distributed locks (such as Redis '
                                                   'Redlock) so only a single worker refreshes the database, alongside '
                                                   'randomized TTL jitter or probabilistic early recomputation.'},
                          'te': {   'concept_score': 9.6,
                                    'text': 'క్యాష్-అసైడ్ లో అప్లికేషన్ ముందుగా క్యాష్ చూసి లేకపోతే డిబి నుండి తెచ్చి '
                                            'స్టోర్ చేస్తుంది. రైట్-త్రూ లో క్యాష్ మరియు డిబి ఒకేసారి అప్\u200cడేట్ '
                                            'అవుతాయి. క్యాష్ స్టాంపేడ్ నివారించడానికి డిస్ట్రిబ్యూటెడ్ లాక్ (రెడిస్ '
                                            'లాక్) లేదా ఎర్లీ బ్యాక్\u200cగ్రౌండ్ రిఫ్రెష్ వాడతాము.'}},
    'title': 'Caching Patterns & Mitigating Cache Stampede'},
    {   'category': 'Security & Identity',
    'difficulty': 'Intermediate',
    'expected_concepts': [   'stateless signature verification vs stateful session lookup',
                             'invalidation challenges with JWT',
                             'short-lived access tokens (15m) + long-lived refresh tokens (7d)',
                             'Refresh Token rotation revoking token family on reuse',
                             'HttpOnly Secure SameSite cookies preventing XSS and CSRF'],
    'id': 'sec-auth-jwt',
    'question': {   'en': 'What are the trade-offs between stateless JWTs and server-side sessions, and how does '
                          'Refresh Token rotation protect against token theft?',
                    'hi': 'स्टेटलेस JWT और सर्वर-साइड सेशन के बीच क्या अंतर है, और रिफ्रेश टोकन रोटेशन टोकन चोरी से '
                          'कैसे बचाता है?',
                    'kn': 'JWT ಮತ್ತು ಸರ್ವರ್-ಸೈಡ್ ಸೆಷನ್\u200cಗಳ ನಡುವಿನ ವ್ಯತ್ಯಾಸಗಳೇನು? ರಿಫ್ರೆಶ್ ಟೋಕನ್ ರೊಟೇಶನ್ '
                          'ಸುರಕ್ಷತೆಯನ್ನು ಹೇಗೆ ಖಚಿತಪಡಿಸುತ್ತದೆ?',
                    'ta': 'JWT மற்றும் சர்வர் பக்க அமர்வுகளுக்கு இடையிலான வேறுபாடுகள் யாவை? புதுப்பிப்பு டோக்கன் '
                          'சுழற்சி எவ்வாறு பாதுகாப்பை வழங்குகிறது?',
                    'te': 'స్టేట్\u200cలెస్ JWT మరియు సర్వర్-సైడ్ సెషన్ల మధ్య తేడాలు ఏమిటి? రిఫ్రెష్ టోకెన్ రొటేషన్ '
                          'టోకెన్ దొంగతనాన్ని ఎలా అరికడుతుంది?'},
    'role': 'fullstack_security',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.8,
                                           'text': 'Stateless JWTs eliminate database session lookups by '
                                                   'cryptographically signing user claims, enabling seamless '
                                                   'horizontal scale, but revocation before expiration is notoriously '
                                                   'difficult. To balance security, we use short-lived access tokens '
                                                   'paired with long-lived refresh tokens stored in HttpOnly SameSite '
                                                   'cookies. Refresh Token Rotation issues a new refresh token on '
                                                   'every exchange and invalidates the entire token family if a '
                                                   'compromised token is reused.'},
                          'te': {   'concept_score': 9.5,
                                    'text': 'జేడబ్ల్యుటి స్టేట్\u200cలెస్ గా పనిచేస్తుంది కాబట్టి డేటాబేస్ లుక్అప్ '
                                            'అవసరం లేదు, కానీ వెంటనే ఇన్వాలిడేట్ చేయడం కష్టం. రిఫ్రెష్ టోకెన్ రొటేషన్ '
                                            'లో ఒకసారి రిఫ్రెష్ టోకెన్ వాడితే వెంటనే కొత్తది ఇస్తాము. పాతది మళ్ళీ '
                                            'వాడితే ఆ మొత్తం టోకెన్ ఫ్యామిలీ ని బ్లాక్ చేస్తాము.'}},
    'title': 'JWT vs Session Authentication & Refresh Token Rotation'},
    {   'category': 'Python & Operating Systems',
    'difficulty': 'Intermediate',
    'expected_concepts': [   'I/O-bound concurrency vs CPU-bound parallelism',
                             'GIL preventing multiple native threads from executing Python bytecode simultaneously',
                             'multiprocessing module for true multi-core CPU parallelism',
                             'asyncio cooperative multitasking via single-threaded event loop',
                             'free-threaded Python 3.13 evolution'],
    'id': 'os-concurrency-gil',
    'question': {   'en': 'How does Python handle concurrency versus parallelism, and what role does the Global '
                          'Interpreter Lock (GIL) play in multithreading?',
                    'hi': 'पायथन में कन्क्रेन्सी और पैरेललिज्म के बीच क्या अंतर है, और ग्लोबल इंटरप्रेटर लॉक (GIL) '
                          'क्या भूमिका निभाता है?',
                    'kn': 'ಪೈಥಾನ್\u200cನಲ್ಲಿ ಕಾನ್ಕರೆನ್ಸಿ ಮತ್ತು ಪ್ಯಾರಲಲಿಸಂ ನಡುವಿನ ವ್ಯತ್ಯಾಸವೇನು? GIL ನ ಪಾತ್ರವೇನು?',
                    'ta': 'பைத்தானில் ஒத்திசைவு (Concurrency) மற்றும் இணையான தன்மை (Parallelism) எவ்வாறு '
                          'கையாளப்படுகிறது? GIL இன் பங்கு என்ன?',
                    'te': 'పైథాన్\u200cలో కాన్\u200cకరెన్సీ మరియు పారలలిజం మధ్య తేడా ఏమిటి? మల్టీథ్రెడింగ్\u200cలో '
                          'గ్లోబల్ ఇంటర్\u200cప్రెటర్ లాక్ (GIL) ఎలాంటి పాత్ర పోషిస్తుంది?'},
    'role': 'python_core',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.8,
                                           'text': 'Concurrency is managing multiple tasks out of phase, whereas '
                                                   'parallelism executes them simultaneously across multi-core '
                                                   'processors. In standard CPython, the Global Interpreter Lock (GIL) '
                                                   'is a mutex that prevents multiple native OS threads from executing '
                                                   'Python bytecode at once, rendering threading ineffective for '
                                                   'CPU-bound computation. Consequently, CPU-heavy tasks rely on the '
                                                   'multiprocessing module, while I/O-bound workloads excel using '
                                                   "asyncio's non-blocking event loop."},
                          'te': {   'concept_score': 9.6,
                                    'text': 'కాన్\u200cకరెన్సీ అంటే ఒకే సమయంలో మల్టిపుల్ టాస్క్స్ పురోగతిలో ఉండటం, '
                                            'పారలలిజం అంటే వేర్వేరు కోర్లలో ఒకేసారి ఎగ్జిక్యూట్ అవ్వడం. పైథాన్ జిఐఎల్ '
                                            '(GIL) వల్ల మల్టీథ్రెడింగ్ సిపియు-బౌండ్ టాస్క్\u200cలకు పనికిరాదు. అందుకే '
                                            'మల్టీప్రాసెసింగ్ లేదా అస్రింక్ఐఓ (asyncio) వాడతాము.'}},
    'title': 'Concurrency, Parallelism, and the Python GIL'},
    {   'category': 'DevOps & SRE',
    'difficulty': 'Intermediate',
    'expected_concepts': [   'Blue-Green dual environments with instant router switch',
                             'Canary incremental traffic rollout (5% -> 25% -> 100%)',
                             'health check validation and instant rollback',
                             'expand-contract (parallel change) database migration pattern',
                             'backward-compatible database schema changes'],
    'id': 'devops-cicd-deploy',
    'question': {   'en': 'How do Blue-Green deployments and Canary releases achieve zero-downtime releases, and how '
                          'do you handle database migrations?',
                    'hi': 'ब्लू-ग्रीन डिप्लॉयमेंट और कैनरी रिलीज़ ज़ीरो-डाउनटाइम कैसे प्राप्त करते हैं? डेटाबेस '
                          'माइग्रेशन को कैसे संभाला जाता है?',
                    'kn': 'ಬ್ಲೂ-ಗ್ರೀನ್ ಮತ್ತು ಕೆನರಿ ನಿಯೋಜನೆಗಳು ಶೂನ್ಯ-ಡೌನ್\u200cಟೈಮ್ ಅನ್ನು ಹೇಗೆ ಸಾಧಿಸುತ್ತವೆ? ಡೇಟಾಬೇಸ್ '
                          'ಮೈಗ್ರೇಶನ್ ಅನ್ನು ಹೇಗೆ ನಿರ್ವಹಿಸುತ್ತೀರಿ?',
                    'ta': 'புளூ-கிரீன் மற்றும் கேனரி வெளியீடுகள் எவ்வாறு பூஜ்ஜிய-நேர முடக்கத்தை (zero-downtime) '
                          'அடைகின்றன? தரவுத்தள மாற்றங்களை எவ்வாறு கையாளுகிறீர்கள்?',
                    'te': 'బ్లూ-గ్రీన్ డిప్లాయ్\u200cమెంట్స్ మరియు కెనరీ రిలీజ్ ద్వారా జీరో-డౌన్\u200cటైమ్ ఎలా '
                          'సాధిస్తారు? డేటాబేస్ మైగ్రేషన్లను ఎలా నిర్వహిస్తారు?'},
    'role': 'devops_sre',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.9,
                                           'text': 'Blue-Green deployments maintain two identical production stacks, '
                                                   'routing 100% of traffic from the active Blue stack to the verified '
                                                   'Green stack via the load balancer for instantaneous switchover. '
                                                   'Canary releases incrementally route traffic (e.g. 5% to 100%) '
                                                   'while monitoring telemetry for error spikes. To prevent downtime '
                                                   'during schema changes, we implement the Expand-Contract pattern, '
                                                   'ensuring new columns are backward-compatible before deprecating '
                                                   'old ones.'},
                          'te': {   'concept_score': 9.7,
                                    'text': 'బ్లూ-గ్రీన్ డిప్లాయ్\u200cమెంట్ లో కొత్త వెర్షన్ ని గ్రీన్ '
                                            'ఎన్విరాన్మెంట్\u200cలో టెస్ట్ చేసి రౌటర్ ని స్విచ్ చేస్తాము. కెనరీ లో '
                                            'కొద్ది శాతం యూజర్లకి మాత్రమే పంపి లాగ్స్ చూస్తాము. డేటాబేస్ లో '
                                            'ఎక్స్\u200cపాండ్-కాంట్రాక్ట్ విధానం ద్వారా పాత మరియు కొత్త వెర్షన్లు '
                                            'రెండింటికీ సపోర్ట్ చేసేలా మైగ్రేషన్ చేస్తాము.'}},
    'title': 'CI/CD Pipelines & Zero-Downtime Deployment Strategies'},
    {   'category': 'Microservices & Reliability',
    'difficulty': 'Advanced',
    'expected_concepts': [   'closed, open, and half-open states',
                             'failure threshold triggering open state',
                             'fast-fail fallback responses without hanging threads',
                             'canary probe requests in half-open state',
                             'bulkhead isolation to protect system resources'],
    'id': 'sys-microservices-resilience',
    'question': {   'en': 'What is the Circuit Breaker pattern in microservices, and how does it prevent cascading '
                          'failures across downstream dependencies?',
                    'hi': 'माइक्रोसर्विस में सर्किट ब्रेकर पैटर्न क्या है, और यह डाउनस्ट्रीम निर्भरताओं में क्रमिक '
                          'विफलता को कैसे रोकता है?',
                    'kn': 'ಮೈಕ್ರೋಸರ್ವಿಸ್\u200cಗಳಲ್ಲಿ ಸರ್ಕ್ಯೂಟ್ ಬ್ರೇಕರ್ ಪ್ಯಾಟರ್ನ್ ಎಂದರೇನು ಮತ್ತು ಇದು ಸರಣಿ ವೈಫಲ್ಯಗಳನ್ನು '
                          'ಹೇಗೆ ತಡೆಯುತ್ತದೆ?',
                    'ta': 'மைக்ரோ சர்வீஸ்களில் சர்க்யூட் பிரேக்கர் பேட்டர்ன் என்றால் என்ன? இது தொடர் தோல்விகளை எவ்வாறு '
                          'தடுக்கிறது?',
                    'te': 'మైక్రోసర్వీసెస్ లో సర్క్యూట్ బ్రేకర్ ప్యాటర్న్ అంటే ఏమిటి? ఇది ఇతర సర్వీసులలో ఫెయిల్యూర్స్ '
                          'వ్యాపించకుండా ఎలా నిరోధిస్తుంది?'},
    'role': 'backend_resilience',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.8,
                                           'text': 'The Circuit Breaker pattern wraps external RPC calls in a state '
                                                   'machine transitioning between Closed, Open, and Half-Open states. '
                                                   'When downstream error rates exceed a threshold, the breaker trips '
                                                   'Open, failing calls immediately with cached fallbacks rather than '
                                                   'consuming thread pools in blocking timeouts. After a cooldown, it '
                                                   'enters Half-Open to probe health, preventing cascading system-wide '
                                                   'outages.'},
                          'te': {   'concept_score': 9.6,
                                    'text': 'సర్క్యూట్ బ్రేకర్ లో క్లోజ్డ్, ఓపెన్, హాఫ్-ఓపెన్ అనే మూడు స్టేట్స్ '
                                            'ఉంటాయి. ఏదైనా డౌన్\u200cస్ట్రీమ్ సర్వీస్ ఫెయిల్ అయినప్పుడు సర్క్యూట్ '
                                            'ఓపెన్ అయి వెంటనే ఫాల్\u200cబ్యాక్ రెస్పాన్స్ ఇస్తుంది. దీనివల్ల థ్రెడ్స్ '
                                            'బ్లాక్ అవ్వకుండా మిగతా సిస్టమ్ సేఫ్ గా ఉంటుంది.'}},
    'title': 'Circuit Breakers & Cascading Failure Isolation'},
    {   'category': 'Database Architecture',
    'difficulty': 'Advanced',
    'expected_concepts': [   'read scaling via asynchronous replica nodes',
                             'write scaling via horizontal partition sharding',
                             'shard key selection (hashing vs range)',
                             'handling replication lag with read-your-own-writes routing',
                             'minimizing distributed cross-shard joins'],
    'id': 'db-sharding-replication',
    'question': {   'en': 'What is the difference between Read Replicas and Database Sharding, and how do you handle '
                          'replication lag and cross-shard queries?',
                    'hi': 'रीड रेप्लिका और डेटाबेस शार्डिंग में क्या अंतर है? रेप्लिकेशन लैग और क्रॉस-शार्ड क्वेरीज़ '
                          'को कैसे संभालते हैं?',
                    'kn': 'ರೀಡ್ ರೆಪ್ಲಿಕಾ ಮತ್ತು ಡೇಟಾಬೇಸ್ ಶಾರ್ಡಿಂಗ್ ನಡುವಿನ ವ್ಯತ್ಯಾಸವೇನು? ರೆಪ್ಲಿಕೇಶನ್ ಲ್ಯಾಗ್ ಅನ್ನು ಹೇಗೆ '
                          'ನಿರ್ವಹಿಸುತ್ತೀರಿ?',
                    'ta': 'ரீட் ரெப்ளிகா மற்றும் தரவுத்தள ஷார்டிங் இடையே உள்ள வித்தியாசம் என்ன? ரெப்ளிகேஷன் லேக் '
                          'சிக்கலை எவ்வாறு தீர்க்கிறீர்கள்?',
                    'te': 'రీడ్ రెప్లికాస్ మరియు డేటాబేస్ షార్డింగ్ మధ్య తేడా ఏమిటి? రెప్లికేషన్ లాగ్ మరియు '
                          'క్రాస్-షార్డ్ క్వెరీలను ఎలా హ్యాండిల్ చేస్తారు?'},
    'role': 'database_engineer',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.9,
                                           'text': 'Read Replicas scale read throughput by asynchronously streaming '
                                                   'WAL changes from the primary master node to worker replicas, but '
                                                   'all writes must still hit the single master. Horizontal Sharding '
                                                   'partitions table rows across distinct database servers using a '
                                                   'shard key, scaling both reads and writes. To prevent stale reads '
                                                   'from replication lag, we route read-your-own-writes queries '
                                                   'directly to the primary database.'},
                          'te': {   'concept_score': 9.7,
                                    'text': 'రీడ్ రెప్లికాస్ రీడ్ ట్రాఫిక్ ని హ్యాండిల్ చేయడానికి క్లోనింగ్ చేస్తాయి, '
                                            'కానీ రైట్ ట్రాఫిక్ ని పెంచలేవు. షార్డింగ్ లో డేటాను వేర్వేరు సర్వర్లలో '
                                            'ముక్కలుగా విభజిస్తాము. రెప్లికేషన్ లాగ్ ఉన్నప్పుడు యూజర్ చేసిన రైట్స్ '
                                            'కోసం ప్రైమరీ డిబి కి మాత్రమే రీడ్స్ పంపుతాము.'}},
    'title': 'Database Scaling: Read Replicas vs Horizontal Sharding'},
    {   'category': 'Real-Time Web Architecture',
    'difficulty': 'Intermediate',
    'expected_concepts': [   'full-duplex bidirectional TCP vs unidirectional server-to-client stream',
                             'HTTP/2 multiplexing compatibility of SSE',
                             'automatic reconnection and message ID tracking in SSE',
                             'lower complexity and firewall friendliness of SSE',
                             'use case: notifications/LLM streaming (SSE) vs multiplayer/chat (WebSocket)'],
    'id': 'web-websockets-sse',
    'question': {   'en': 'Compare WebSockets, Server-Sent Events (SSE), and Short/Long Polling for real-time web '
                          'applications. When is SSE the better choice?',
                    'hi': 'रीयल-टाइम वेब ऐप्स के लिए WebSockets, SSE और पोलिंग की तुलना करें। SSE कब बेहतर विकल्प है?',
                    'kn': 'ರಿಯಲ್-ಟೈಮ್ ವೆಬ್ ಅಪ್ಲಿಕೇಶನ್\u200cಗಳಿಗಾಗಿ WebSockets, SSE ಮತ್ತು ಪೋಲಿಂಗ್ ಅನ್ನು ಹೋಲಿಸಿ. SSE '
                          'ಯಾವಾಗ ಉತ್ತಮ ಆಯ್ಕೆ?',
                    'ta': 'WebSockets, Server-Sent Events (SSE) மற்றும் போலிங் (Polling) ஆகியவற்றை ஒப்பிடுக. SSE '
                          'எப்போது சிறந்த தேர்வாகும்?',
                    'te': 'రియల్-టైమ్ వెబ్ అప్లికేషన్ల కోసం WebSockets, Server-Sent Events (SSE), మరియు పోలింగ్ లను '
                          'సరిపోల్చండి. SSE ఎప్పుడు ఉత్తమ ఎంపిక?'},
    'role': 'frontend_fullstack',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.8,
                                           'text': 'WebSockets establish a persistent, full-duplex TCP socket outside '
                                                   'standard HTTP request-response semantics, ideal for high-frequency '
                                                   'bidirectional interactions like chat or multiplayer games. '
                                                   'Server-Sent Events (SSE) provide a unidirectional, text-based HTTP '
                                                   'stream with native automatic reconnection and message IDs. For LLM '
                                                   'token streaming, financial ticker updates, and notifications, SSE '
                                                   'is superior due to lower operational complexity and native HTTP/2 '
                                                   'multiplexing.'},
                          'te': {   'concept_score': 9.6,
                                    'text': 'వెబ్\u200cసాకెట్ ఫుల్-డూప్లెక్స్ బైడైరెక్షనల్ కమ్యూనికేషన్ ఇస్తుంది, ఇది '
                                            'చాట్ మరియు గేమింగ్ కి మంచిది. ఎస్ఎస్ఈ (SSE) కేవలం సర్వర్ నుండి క్లయింట్ '
                                            'కి డేటా పంపుతుంది, హెచ్\u200cటిటిపి ప్రోటోకాల్ మీదే నడుస్తుంది. '
                                            'నోటిఫికేషన్లు లేదా ఎల్\u200cఎల్\u200cఎమ్ టోకెన్ స్ట్రీమింగ్ కి SSE చాలా '
                                            'సింపుల్ మరియు బెస్ట్.'}},
    'title': 'Real-Time Protocols: WebSockets vs Server-Sent Events (SSE)'},
    {   'category': 'Distributed Systems & Security',
    'difficulty': 'Intermediate',
    'expected_concepts': [   'Token Bucket capacity and refill rate allowing controlled bursts',
                             'Sliding Window Log timestamp precision vs memory usage',
                             'Sliding Window Counter hybrid approximation',
                             'Redis Lua scripts for atomic increment and expiry checks',
                             'HTTP 429 Too Many Requests with Retry-After headers'],
    'id': 'sys-rate-limiting',
    'question': {   'en': 'How do Token Bucket and Sliding Window Log rate-limiting algorithms work, and how do you '
                          'implement distributed rate limiting using Redis?',
                    'hi': 'टोकन बकेट और स्लाइडिंग विंडो रेट-लिमिटिंग एल्गोरिदम कैसे काम करते हैं? Redis का उपयोग करके '
                          'इसे कैसे लागू किया जाता है?',
                    'kn': 'ಟೋಕನ್ ಬಕೆಟ್ ಮತ್ತು ಸ್ಲೈಡಿಂಗ್ ವಿಂಡೋ ರೇಟ್-ಲಿಮಿಟಿಂಗ್ ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತವೆ? Redis ಬಳಸಿ '
                          'ಇದನ್ನು ಹೇಗೆ ಜಾರಿಗೊಳಿಸುತ್ತೀರಿ?',
                    'ta': 'டோக்கன் பக்கெட் மற்றும் ஸ்லைடிங் விண்டோ ரேட்-லிமிட்டிங் எவ்வாறு செயல்படுகின்றன? Redis மூலம் '
                          'விநியோகிக்கப்பட்ட ரேட் லிமிட்டிங் எவ்வாறு செயல்படுத்தப்படுகிறது?',
                    'te': 'టోకెన్ బకెట్ మరియు స్లైడింగ్ విండో రేట్-లిమిటింగ్ అల్గోరిథంలు ఎలా పనిచేస్తాయి? రెడిస్ '
                          '(Redis) ఉపయోగించి డిస్ట్రిబ్యూటెడ్ రేట్ లిమిటింగ్ ఎలా అమలు చేస్తారు?'},
    'role': 'backend_gateway',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.8,
                                           'text': 'The Token Bucket algorithm accumulates tokens at a constant refill '
                                                   'rate up to a maximum burst capacity, dropping requests when empty. '
                                                   'The Sliding Window Counter approximates exact timestamps by '
                                                   'weighting request counts across current and previous time slices. '
                                                   'In distributed gateways, we execute atomic Redis Lua scripts to '
                                                   'increment counters and enforce TTLs, returning standard HTTP 429 '
                                                   'with Retry-After headers to prevent denial-of-service spikes.'},
                          'te': {   'concept_score': 9.5,
                                    'text': 'టోకెన్ బకెట్ లో స్థిరమైన రేటుతో టోకెన్స్ యాడ్ అవుతాయి, రిక్వెస్ట్ '
                                            'వచ్చినప్పుడు టోకెన్ తీసుకుంటుంది. రెడిస్ లో పరమాణు (Atomic) ఆపరేషన్స్ '
                                            'కోసం లువా (Lua) స్క్రిప్ట్ వాడి కౌంటర్ చెక్ చేస్తాము. లిమిట్ దాటితే '
                                            'హెచ్\u200cటిటిపి 429 రెస్పాన్స్ పంపుతాము.'}},
    'title': 'API Rate Limiting Algorithms in Distributed Environments'},
    {   'category': 'Cloud & Kubernetes',
    'difficulty': 'Intermediate',
    'expected_concepts': [   'Pending, Running, Succeeded, Failed, CrashLoopBackOff',
                             'Liveness probe restarting unhealthy containers',
                             'Readiness probe controlling traffic routing via Service endpoints',
                             'Startup probe protecting slow initialization workloads',
                             'Horizontal Pod Autoscaler (HPA) responding to CPU/memory metrics'],
    'id': 'cloud-k8s-pod-lifecycle',
    'question': {   'en': 'Explain the lifecycle of a Kubernetes Pod. What is the difference between liveness, '
                          'readiness, and startup probes?',
                    'hi': 'कुबेरनेट्स पॉड के जीवन चक्र को समझाएं। लाइवनेस, रेडीनेस और स्टार्टअप प्रोब्स में क्या अंतर '
                          'है?',
                    'kn': 'ಕುಬರ್ನೆಟಿಸ್ ಪಾಡ್ ಲೈಫ್\u200cಸೈಕಲ್ ವಿವರಿಸಿ. ಲೈವ್\u200cನೆಸ್ ಮತ್ತು ರೆಡಿನೆಸ್ ಪ್ರೋಬ್\u200cಗಳ '
                          'ನಡುವಿನ ವ್ಯತ್ಯಾಸವೇನು?',
                    'ta': 'குபெர்னெட்ஸ் பாட் (Pod) வாழ்க்கைச் சுழற்சியை விளக்குக. லைவ்னஸ் மற்றும் ரெடினஸ் '
                          'ப்ரோப்களுக்கு இடையே உள்ள வேறுபாடு என்ன?',
                    'te': 'కుబెర్\u200cనెటీస్ పాడ్ (Pod) లైఫ్\u200cసైకిల్ వివరించండి. లైవ్\u200cనెస్, రెడీనెస్ మరియు '
                          'స్టార్టప్ ప్రోబ్స్ మధ్య తేడా ఏమిటి?'},
    'role': 'devops_kubernetes',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.8,
                                           'text': 'A Kubernetes Pod progresses through phases from Pending to Running '
                                                   'or CrashLoopBackOff. Liveness probes detect deadlocks, restarting '
                                                   'containers when checks fail; Readiness probes determine whether '
                                                   'the pod is primed to accept user traffic, removing failed pods '
                                                   'from Service endpoints without restarting them. Startup probes '
                                                   'disable liveness checks during lengthy initializations, ensuring '
                                                   'reliable deployments under Horizontal Pod Autoscaling.'},
                          'te': {   'concept_score': 9.6,
                                    'text': 'పాడ్ పెండింగ్ నుండి రన్నింగ్ స్టేట్ కి మారుతుంది. లైవ్\u200cనెస్ ప్రోబ్ '
                                            'ఫెయిల్ అయితే కంటైనర్ రీస్టార్ట్ అవుతుంది. రెడీనెస్ ప్రోబ్ పాడ్ ట్రాఫిక్ '
                                            'తీసుకోవడానికి సిద్ధంగా ఉందో లేదో చెక్ చేస్తుంది, సిద్ధంగా లేకపోతే '
                                            'ట్రాఫిక్ ని నిలిపివేస్తుంది.'}},
    'title': 'Kubernetes Pod Lifecycle, Probes, and Auto-scaling'},
    {   'category': 'Message Queues & Streaming',
    'difficulty': 'Advanced',
    'expected_concepts': [   'Kafka append-only partitioned commit log with replayability',
                             'RabbitMQ smart broker dumb consumer routing via exchanges',
                             'consumer offset management in Kafka',
                             'message deletion upon consumer ACK in RabbitMQ',
                             'high-throughput analytics streaming vs complex task routing'],
    'id': 'msg-kafka-rabbitmq',
    'question': {   'en': 'What is the fundamental architectural difference between Apache Kafka and RabbitMQ? When '
                          'would you select an event log over a message broker?',
                    'hi': 'अपाचे काफ्का और रैबिटएमक्यू के बीच क्या मौलिक अंतर है? आप मैसेज ब्रोकर की तुलना में इवेंट '
                          'लॉग कब चुनेंगे?',
                    'kn': 'ಅಪಾಚೆ ಕಾಫ್ಕಾ ಮತ್ತು ರ್ಯಾಬಿಟ್\u200cಎಂಕ್ಯೂ ನಡುವಿನ ವ್ಯತ್ಯಾಸವೇನು? ಸಂದೇಶ ಬ್ರೋಕರ್ ಬದಲಿಗೆ ಈವೆಂಟ್ '
                          'ಲಾಗ್ ಅನ್ನು ಯಾವಾಗ ಆರಿಸಿಕೊಳ್ಳುತ್ತೀರಿ?',
                    'ta': 'அப்பாச்சி காஃப்கா மற்றும் ராபிட்எம்ப்யூ இடையே உள்ள கட்டமைப்பு வேறுபாடு என்ன? மெசேஜ் '
                          'ப்ரோக்கருக்குப் பதிலாக நிகழ்வுப் பதிவை (Event Log) எப்போது தேர்ந்தெடுப்பீர்கள்?',
                    'te': 'అపాచీ కాఫ్కా (Kafka) మరియు రాబిట్\u200cఎంక్యూ (RabbitMQ) మధ్య ఉన్న ప్రాథమిక తేడా ఏమిటి? '
                          'మెసేజ్ బ్రోకర్ కంటే ఈవెంట్ లాగ్ ని ఎప్పుడు ఎంచుకుంటారు?'},
    'role': 'backend_data',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.9,
                                           'text': 'Kafka is a distributed, append-only partitioned commit log where '
                                                   'messages are retained by time and consumers track their own '
                                                   'offsets, enabling replayability and massive parallel streaming '
                                                   'throughput. RabbitMQ is an AMQP message broker with exchanges and '
                                                   'queues where the broker actively manages delivery and removes '
                                                   'messages upon consumer acknowledgment. Kafka excels for event '
                                                   'sourcing and streaming analytics, while RabbitMQ is superior for '
                                                   'granular task routing.'},
                          'te': {   'concept_score': 9.7,
                                    'text': 'కాఫ్కా అనేది అపెండ్-ఓన్లీ డిస్ట్రిబ్యూటెడ్ కమిట్ లాగ్. ఇందులో మెసేజెస్ '
                                            'డిలీట్ అవ్వవు, మళ్ళీ రీప్లే చేసుకోవచ్చు. రాబిట్\u200cఎంక్యూ లో కన్స్యూమర్ '
                                            'యాక్ చేశాక మెసేజ్ డిలీట్ అవుతుంది. హై త్రూపుట్ ఈవెంట్ స్ట్రీమింగ్ కోసం '
                                            'కాఫ్కా, కాంప్లెక్స్ రౌటింగ్ టాస్క్స్ కోసం రాబిట్\u200cఎంక్యూ బెస్ట్.'}},
    'title': 'Kafka Log Partitioning vs RabbitMQ AMQP Queues'},
    {   'category': 'System Design',
    'difficulty': 'Advanced',
    'expected_concepts': [   'presigned S3 upload URLs direct from client to object storage',
                             'bypassing application server memory and I/O bottlenecks',
                             'multipart uploads with chunked retry for large files',
                             'S3 event notifications triggering asynchronous worker transcoding',
                             'CloudFront CDN caching for media delivery'],
    'id': 'sys-design-cdn-s3',
    'question': {   'en': 'How would you design a high-throughput file upload service that handles millions of user '
                          'uploads securely without choking application servers?',
                    'hi': 'आप एक हाई-थ्रूपुट फ़ाइल अपलोड सेवा कैसे डिज़ाइन करेंगे जो एप्लिकेशन सर्वर को ब्लॉक किए बिना '
                          'लाखों फ़ाइलों को सुरक्षित रूप से संभाल सके?',
                    'kn': 'ಅಪ್ಲಿಕೇಶನ್ ಸರ್ವರ್\u200cಗಳ ಮೇಲೆ ಒತ್ತಡ ಬೀರದಂತೆ ಲಕ್ಷಾಂತರ ಫೈಲ್ ಅಪ್\u200cಲೋಡ್\u200cಗಳನ್ನು '
                          'ಸುರಕ್ಷಿತವಾಗಿ ನಿರ್ವಹಿಸುವ ವ್ಯವಸ್ಥೆಯನ್ನು ಹೇಗೆ ವಿನ್ಯಾಸಗೊಳಿಸುತ್ತೀರಿ?',
                    'ta': 'பயன்பாட்டு சேவையகங்களை முடக்காமல் மில்லியன் கணக்கான கோப்பு பதிவேற்றங்களை பாதுகாப்பாக '
                          'கையாளும் அமைப்பை எவ்வாறு வடிவமைப்பீர்கள்?',
                    'te': 'అప్లికేషన్ సర్వర్లపై భారం పడకుండా మిలియన్ల కొద్దీ యూజర్ ఫైల్ అప్\u200cలోడ్\u200cలను '
                          'సురక్షితంగా నిర్వహించే హై-త్రూపుట్ సిస్టమ్\u200cను ఎలా డిజైన్ చేస్తారు?'},
    'role': 'system_design',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.9,
                                           'text': 'To bypass application server I/O and memory saturation, the client '
                                                   'requests a short-lived presigned upload URL from the API, '
                                                   'uploading chunks directly to cloud object storage (e.g. AWS S3) '
                                                   'via multipart uploads. S3 event notifications trigger asynchronous '
                                                   'serverless lambdas or message queues to sanitize, virus-scan, and '
                                                   'transcode the assets, distributing processed media through a '
                                                   'global CloudFront CDN edge cache.'},
                          'te': {   'concept_score': 9.8,
                                    'text': 'ఫైల్స్ ని డైరెక్ట్ గా అప్లికేషన్ సర్వర్ కి పంపకుండా, బ్యాకెండ్ నుండి '
                                            'ప్రీ-సైన్డ్ ఎస్3 (S3) యుఆర్ఎల్ ఇస్తాము. బ్రౌజర్ డైరెక్ట్ గా ఎస్3 కి '
                                            'అప్\u200cలోడ్ చేస్తుంది. అప్\u200cలోడ్ పూర్తి కాగానే ఎస్3 ఈవెంట్ ద్వారా '
                                            'బ్యాక్\u200cగ్రౌండ్ వర్కర్ ప్రాసెస్ చేసి సిడిఎన్ (CDN) ద్వారా డెలివరీ '
                                            'చేస్తాము.'}},
    'title': 'System Design: Scaling Large Media & File Uploads'},
    {   'category': 'Web Security',
    'difficulty': 'Intermediate',
    'expected_concepts': [   'SQLi mitigated by parameterized queries / ORM prepared statements',
                             'XSS mitigated by automatic context-aware HTML escaping and Content Security Policy (CSP)',
                             'CSRF mitigated by Anti-CSRF tokens and SameSite=Strict cookies',
                             'CORS headers restricting cross-origin fetch requests',
                             'defense in depth principle'],
    'id': 'sec-web-vulnerabilities',
    'question': {   'en': 'Explain the root causes of SQL Injection, Cross-Site Scripting (XSS), and Cross-Site '
                          'Request Forgery (CSRF). How do modern frameworks mitigate them?',
                    'hi': 'SQL इंजेक्शन, XSS और CSRF के मुख्य कारण क्या हैं? आधुनिक फ्रेमवर्क इन्हें कैसे रोकते हैं?',
                    'kn': 'SQL ಇಂಜೆಕ್ಷನ್, XSS ಮತ್ತು CSRF ನ ಮೂಲ ಕಾರಣಗಳೇನು? ಆಧುನಿಕ ಫ್ರೇಮ್\u200cವರ್ಕ್\u200cಗಳು ಇವುಗಳನ್ನು '
                          'ಹೇಗೆ ತಡೆಯುತ್ತವೆ?',
                    'ta': 'SQL Injection, XSS, மற்றும் CSRF ஆகியவற்றின் மூலக் காரணங்கள் யாவை? நவீன கட்டமைப்புகள் '
                          'எவ்வாறு இவற்றைத் தடுக்கின்றன?',
                    'te': 'SQL ఇంజెక్షన్, XSS, మరియు CSRF సమస్యల మూల కారణాలు ఏమిటి? ఆధునిక ఫ్రేమ్\u200cవర్కులు వీటిని '
                          'ఎలా నిరోధిస్తాయి?'},
    'role': 'security_engineer',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.8,
                                           'text': 'SQL Injection occurs when untrusted input is interpolated into '
                                                   'dynamic queries, solved definitively by parameterized prepared '
                                                   'statements. Cross-Site Scripting (XSS) injects malicious scripts '
                                                   'into user browsers, mitigated via context-aware HTML entity '
                                                   'escaping and strict Content Security Policies. Cross-Site Request '
                                                   'Forgery (CSRF) exploits ambient browser session credentials, '
                                                   'resolved using crypto anti-CSRF synchronizer tokens and '
                                                   'SameSite=Strict cookies.'},
                          'te': {   'concept_score': 9.6,
                                    'text': 'యూజర్ ఇన్\u200cపుట్ ని నేరుగా ఎస్\u200cక్యూఎల్ లో కలపడం వల్ల '
                                            'ఎస్\u200cక్యూఎల్ ఇంజెక్షన్ వస్తుంది, దీన్ని పారామీటరైజ్డ్ క్వెరీస్ తో '
                                            'అరికడతాము. ఎక్స్\u200cఎస్\u200cఎస్ (XSS) ని బ్రౌజర్ ఎస్కేపింగ్ మరియు CSP '
                                            'ద్వారా, CSRF ని సేమ్\u200cసైట్ కుకీస్ మరియు CSRF టోకెన్లతో '
                                            'నిరోధిస్తాము.'}},
    'title': 'Mitigating SQL Injection, XSS, and CSRF'},
    {   'category': 'Computer Systems',
    'difficulty': 'Intermediate',
    'expected_concepts': [   'reference counting deallocating immediately at zero count',
                             'generational garbage collection (Gen 0, 1, 2)',
                             'cyclic reference detection using graph traversal / mark-and-sweep',
                             'stop-the-world pauses vs concurrent background sweeps',
                             'memory fragmentation and compacting collectors'],
    'id': 'os-memory-gc',
    'question': {   'en': 'How does automatic Garbage Collection work in high-level runtimes (like Python or V8), and '
                          'how do engines resolve cyclic references?',
                    'hi': 'पायथन या V8 जैसे रनटाइम में गारबेज कलेक्शन कैसे काम करता है, और वे साइक्लिक रेफरेंस को कैसे '
                          'संभालते हैं?',
                    'kn': 'ಪೈಥಾನ್ ಅಥವಾ V8 ರನ್\u200cಟೈಮ್\u200cನಲ್ಲಿ ಗಾರ್ಬೇಜ್ ಕಲೆಕ್ಷನ್ ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ? '
                          'ಸೈಕ್ಲಿಕ್ ರೆಫರೆನ್ಸ್\u200cಗಳನ್ನು ಹೇಗೆ ನಿರ್ವಹಿಸಲಾಗುತ್ತದೆ?',
                    'ta': 'பைத்தான் அல்லது V8 போன்ற சூழல்களில் ஆட்டோமேட்டிக் கார்பேஜ் கலெக்ஷன் எவ்வாறு செயல்படுகிறது? '
                          'சுழற்சி குறிப்புகளை (Cyclic References) எவ்வாறு கையாளுகிறது?',
                    'te': 'పైథాన్ లేదా V8 వంటి రన్\u200cటైమ్స్\u200cలో ఆటోమేటిక్ గార్బేజ్ కలెక్షన్ ఎలా పనిచేస్తుంది? '
                          'సైక్లిక్ రిఫరెన్సులను ఇంజిన్ ఎలా పరిష్కరిస్తుంది?'},
    'role': 'core_software',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.8,
                                           'text': 'Python relies primarily on reference counting for deterministic, '
                                                   "instantaneous deallocation the moment an object's count reaches "
                                                   'zero. To resolve isolated cyclic reference loops where objects '
                                                   'reference each other, Python layers a generational cyclic garbage '
                                                   'collector that periodically traverses object pointer graphs, '
                                                   'segregating objects into three generations to focus sweeping '
                                                   'effort on short-lived allocations.'},
                          'te': {   'concept_score': 9.5,
                                    'text': 'పైథాన్ లో మెయిన్ గా రిఫరెన్స్ కౌంటింగ్ ఉంటుంది, కౌంట్ సున్నా కాగానే మెమరీ '
                                            'రిలీజ్ అవుతుంది. సైక్లిక్ రిఫరెన్సెస్ (రెండు ఆబ్జెక్ట్స్ ఒకదానికొకటి '
                                            'రిఫర్ చేసుకున్నప్పుడు) సాల్వ్ చేయడానికి జెనరేషనల్ గార్బేజ్ కలెక్టర్ '
                                            'గ్రాఫ్ ట్రావర్సల్ ద్వారా గుర్తిస్తుంది.'}},
    'title': 'Memory Management & Garbage Collection Mechanics'},
    {   'category': 'Engineering Practices',
    'difficulty': 'Foundational',
    'expected_concepts': [   'Merge creating a non-destructive 3-way merge commit',
                             'Rebase replaying feature commits on top of base branch for linear history',
                             'golden rule: never rebase public shared branches',
                             'interactive rebase (squash, fixup) for clean PR commits',
                             'fast-forward merges in trunk-based development'],
    'id': 'git-branching-rebase',
    'question': {   'en': 'What is the difference between Git Merge and Git Rebase? When should you prefer a rebase '
                          'workflow in a team environment?',
                    'hi': 'गिट मर्ज और गिट रीबेस के बीच क्या अंतर है? टीम में रीबेस वर्कफ़्लो कब चुनना चाहिए?',
                    'kn': 'Git Merge ಮತ್ತು Git Rebase ನಡುವಿನ ವ್ಯತ್ಯಾಸವೇನು? ತಂಡದಲ್ಲಿ ರೀಬೇಸ್ ವರ್ಕ್\u200cಫ್ಲೋ ಅನ್ನು ಯಾವಾಗ '
                          'ಬಳಸಬೇಕು?',
                    'ta': 'Git Merge மற்றும் Git Rebase இடையே உள்ள வேறுபாடு என்ன? ஒரு குழுவில் ரீபேஸ் பணிப்பாய்வை '
                          'எப்போது விரும்ப வேண்டும்?',
                    'te': 'గిట్ మెర్జ్ (Git Merge) మరియు గిట్ రీబేస్ (Git Rebase) మధ్య తేడా ఏమిటి? టీమ్\u200cలో '
                          'పనిచేసేటప్పుడు రీబేస్ వర్క్\u200cఫ్లోను ఎప్పుడు ఎంచుకుంటారు?'},
    'role': 'software_engineer',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.8,
                                           'text': 'Git Merge preserves chronological truth by creating a '
                                                   'non-destructive 3-way merge commit tying two branch histories '
                                                   'together. Git Rebase rewrites commit history by replaying local '
                                                   'feature commits sequentially on top of the target base branch, '
                                                   'yielding a clean, linear commit log. Feature branches should be '
                                                   'rebased and squashed before pull requests, but shared public '
                                                   'branches must never be rebased.'},
                          'te': {   'concept_score': 9.5,
                                    'text': 'మెర్జ్ అనేది పాత హిస్టరీని అలాగే ఉంచుతూ ఒక కొత్త మెర్జ్ కమిట్ ని క్రియేట్ '
                                            'చేస్తుంది. రీబేస్ మన బ్రాంచ్ కమిట్స్\u200cని మెయిన్ బ్రాంచ్ తాజా కమిట్స్ '
                                            'పై మళ్ళీ అప్లై చేసి లీనియర్ హిస్టరీని ఇస్తుంది. పబ్లిక్ బ్రాంచ్\u200cలపై '
                                            'ఎప్పుడూ రీబేస్ చేయకూడదు.'}},
    'title': 'Git Rebase vs Merge & Trunk-Based Development'},
    {   'category': 'System Design & Networking',
    'difficulty': 'Intermediate',
    'expected_concepts': [   'Round Robin uniform rotation without health weighting',
                             'Least Connections directing load to least busy node',
                             'Consistent Hashing on a hash ring',
                             'minimizing cache remap churn when servers join or leave',
                             'virtual nodes for even distribution across nodes'],
    'id': 'sys-load-balancing',
    'question': {   'en': 'Compare Round Robin, Least Connections, and Consistent Hashing load balancing algorithms. '
                          'When is Consistent Hashing critical?',
                    'hi': 'राउंड रॉबिन, लीस्ट कनेक्शन्स और कंसिस्टेंट हैशिंग लोड बैलेंसिंग एल्गोरिदम की तुलना करें। '
                          'कंसिस्टेंट हैशिंग कब महत्वपूर्ण है?',
                    'kn': 'ಲೋಡ್ ಬ್ಯಾಲೆನ್ಸಿಂಗ್ ಅಲ್ಗಾರಿದಮ್\u200cಗಳನ್ನು ಹೋಲಿಸಿ. ಕನ್ಸಿಸ್ಟೆಂಟ್ ಹ್ಯಾಶಿಂಗ್ ಯಾವಾಗ '
                          'ನಿರ್ಣಾಯಕವಾಗಿರುತ್ತದೆ?',
                    'ta': 'லோட் பேலன்சிங் அல்காரிதம்களை ஒப்பிடுக. கன்சிஸ்டென்ட் ஹாஷிங் எப்போது மிகவும் முக்கியமானது?',
                    'te': 'రౌండ్ రాబిన్, లీస్ట్ కనెక్షన్స్, మరియు కన్సిస్టెంట్ హ్యాషింగ్ లోడ్ బ్యాలెన్సింగ్ పద్ధతులను '
                          'సరిపోల్చండి. కన్సిస్టెంట్ హ్యాషింగ్ ఎప్పుడు చాలా ముఖ్యం?'},
    'role': 'devops_networking',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.8,
                                           'text': 'Round Robin rotates requests sequentially across servers '
                                                   'regardless of request duration; Least Connections dynamically '
                                                   'routes new requests to servers with the fewest active TCP '
                                                   'connections. Consistent Hashing maps both servers and request keys '
                                                   'to positions on a virtual ring; when a node fails or scales up, '
                                                   'only a fraction of keys are remapped, making it critical for '
                                                   'distributed caching tiers like Memcached or DynamoDB.'},
                          'te': {   'concept_score': 9.6,
                                    'text': 'రౌండ్ రాబిన్ వరుసగా అన్ని సర్వర్లకి రిక్వెస్ట్స్ పంపుతుంది. లీస్ట్ '
                                            'కనెక్షన్స్ తక్కువ లోడ్ ఉన్న సర్వర్\u200cని ఎంచుకుంటుంది. కన్సిస్టెంట్ '
                                            'హ్యాషింగ్ అనేది డిస్ట్రిబ్యూటెడ్ క్యాష్ క్లస్టర్లలో సర్వర్ యాడ్ లేదా '
                                            'రిమూవ్ అయినప్పుడు డేటా రీమ్యాపింగ్ అతి తక్కువగా ఉండటానికి చాలా కీలకం.'}},
    'title': 'Load Balancing Algorithms: Round Robin to Consistent Hashing'},
    {   'category': 'Behavioral & Leadership',
    'difficulty': 'Foundational',
    'expected_concepts': [   'STAR method (Situation, Task, Action, Result)',
                             'data-driven proof of concept over personal bias',
                             'active listening and seeking common business objectives',
                             'disagree and commit principle once decision is formalized',
                             'preserving team psychological safety and trust'],
    'id': 'star-team-conflict',
    'question': {   'en': 'Tell me about a time you strongly disagreed with a teammate or lead regarding a technical '
                          'decision. How did you resolve the conflict constructively?',
                    'hi': 'किसी तकनीकी निर्णय पर अपनी टीम के साथी के साथ असहमति के अनुभव का वर्णन करें। आपने इसे '
                          'रचनात्मक रूप से कैसे सुलझाया?',
                    'kn': 'ತಾಂತ್ರಿಕ ನಿರ್ಧಾರದಲ್ಲಿ ಸಹೋದ್ಯೋಗಿಯೊಂದಿಗೆ ಭಿನ್ನಾಭಿಪ್ರಾಯವಿದ್ದ ಸಂದರ್ಭವನ್ನು ವಿವರಿಸಿ. ಅದನ್ನು ನೀವು '
                          'ಹೇಗೆ ರಚನಾತ್ಮಕವಾಗಿ ಪರಿಹರಿಸಿದ್ದೀರಿ?',
                    'ta': 'தொழில்நுட்ப முடிவில் சக ஊழியருடன் முரண்பட்ட அனுபவத்தை விளக்குக. அதை எவ்வாறு சுமூகமாக '
                          'தீர்த்தீர்கள்?',
                    'te': 'ఒక సాంకేతిక లేదా ఆర్కిటెక్చరల్ నిర్ణయంపై మీ సహోద్యోగితో విభేదించిన సందర్భాన్ని వివరించండి. '
                          'ఆ సమస్యను మీరు నిర్మాణాత్మకంగా ఎలా పరిష్కరించారు?'},
    'role': 'engineering_culture',
    'sample_answers': {   'en_golden': {   'fluency_score': 9.9,
                                           'text': 'When deciding on a storage layer, a senior peer favored MongoDB '
                                                   'while I advocated PostgreSQL for strict relational schemas. Rather '
                                                   'than debating opinions, I proposed a timeboxed proof-of-concept '
                                                   'benchmarking realistic query profiles. The empirical latency data '
                                                   'demonstrated PostgreSQL reduced join complexity by 40%. The team '
                                                   'aligned on the data, and we documented the decision in an '
                                                   'Architectural Decision Record (ADR).'},
                          'te': {   'concept_score': 9.6,
                                    'text': 'మా టీమ్\u200cలో ఒకరు మాంగోడిబి వాడాలని, నేను పోస్ట్\u200cగ్రెస్ వాడాలని '
                                            'అనుకున్నాము. నేను ఇద్దరం కలిసి ఒక చిన్న ప్రూఫ్ ఆఫ్ కాన్సెప్ట్ (PoC) చేసి, '
                                            'క్వెరీ పెర్ఫార్మెన్స్ మరియు డేటా రిలేషన్స్ ని టెస్ట్ చేశాము. డేటా ఆధారంగా '
                                            'పోస్ట్\u200cగ్రెస్ మంచిదని అందరం అంగీకరించి ముందుకు వెళ్ళాము.'}},
    'title': 'Resolving Conflicting Technical Architectural Opinions (STAR)'}
]

DYNAMIC_QUESTIONS_REGISTRY: Dict[str, Dict[str, Any]] = {}

class QuestionEngine:
    @staticmethod
    def get_all_questions() -> List[Dict[str, Any]]:
        return list(BASE_QUESTIONS) + list(DYNAMIC_QUESTIONS_REGISTRY.values())

    @staticmethod
    def get_question_by_id(question_id: str) -> Optional[Dict[str, Any]]:
        if question_id in DYNAMIC_QUESTIONS_REGISTRY:
            return DYNAMIC_QUESTIONS_REGISTRY[question_id]
        for q in BASE_QUESTIONS:
            if q["id"] == question_id:
                return q
        return BASE_QUESTIONS[0]

    @staticmethod
    def generate_session_questions(
        role: str = "Full Stack Engineer",
        experience_level: str = "fresher",
        candidate_profile: Optional[Dict[str, Any]] = None,
        duration_minutes: int = 30,
        interview_type: str = "technical",
        count: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Generates dynamic, authentic interview questions using Gemini AI or Smart Contextual Engine."""
        candidate_profile = candidate_profile or {}

        # Determine target question count based on interview duration
        if count is not None and count > 0:
            target_count = count
        elif duration_minutes <= 15:
            target_count = 5
        elif duration_minutes <= 30:
            target_count = 8
        else:
            target_count = 12

        # 1. Try Gemini Generative AI if API key is provided
        gemini_key = candidate_profile.get("gemini_api_key") or os.getenv("GEMINI_API_KEY", "")
        if gemini_key and gemini_key.strip():
            try:
                from services.gemini_generator import generate_interview_questions_with_gemini
                ai_questions = generate_interview_questions_with_gemini(
                    role=role,
                    experience_level=experience_level,
                    candidate_profile=candidate_profile,
                    duration_minutes=duration_minutes,
                    interview_type=interview_type,
                    target_count=target_count,
                    api_key=gemini_key.strip()
                )
                if ai_questions and len(ai_questions) > 0:
                    for q in ai_questions:
                        DYNAMIC_QUESTIONS_REGISTRY[q["id"]] = q
                    return ai_questions
            except Exception as e:
                print(f"⚠️ Gemini Question Generation failed, falling back to smart contextual generator: {e}")

        # 2. Bespoke Smart Contextual Generator (Free, non-repeating, deeply tailored to resume, project, JD & notes)
        from services.gemini_generator import synthesize_smart_contextual_questions
        contextual_questions = synthesize_smart_contextual_questions(
            role=role,
            experience_level=experience_level,
            candidate_profile=candidate_profile,
            duration_minutes=duration_minutes,
            interview_type=interview_type,
            target_count=target_count
        )
        for q in contextual_questions:
            DYNAMIC_QUESTIONS_REGISTRY[q["id"]] = q
        return contextual_questions
