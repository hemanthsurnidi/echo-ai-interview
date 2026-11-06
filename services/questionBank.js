/**
 * ECHO — Curated Bilingual Technical & HR Question Bank
 * 
 * Provides carefully structured questions across domains, with:
 * - English, Telugu, Hindi, and Tamil prompts
 * - Expected technical concepts
 * - Realistic candidate sample responses for simulation mode
 * - Golden English articulation frames
 */

const QUESTION_BANK = [
  {
    id: 'py-list-tuple',
    category: 'Python & Backend',
    role: 'Python Developer / Backend Engineer',
    difficulty: 'Foundational',
    title: 'Difference between Lists and Tuples in Python',
    question: {
      en: 'Explain the difference between Lists and Tuples in Python. When would you use one over the other?',
      te: 'పైథాన్‌లో లిస్ట్‌లు మరియు ట్యుపుల్స్ మధ్య తేడా ఏమిటి? ఒకదానికి బదులు మరొకదాన్ని ఎప్పుడు ఉపయోగిస్తారు?',
      hi: 'पायथन में लिस्ट और टुपल के बीच क्या अंतर है? आप एक के बजाय दूसरे का उपयोग कब करेंगे?',
      ta: 'பைத்தானில் பட்டியல்கள் மற்றும் டூப்பிள்களுக்கு இடையே உள்ள வித்தியாசம் என்ன? ஒன்றை எப்போது மற்றொன்றை விட பயன்படுத்துவீர்கள்?'
    },
    expectedConcepts: [
      'mutability vs immutability',
      'syntax [] vs ()',
      'memory overhead & performance',
      'hashability / dictionary keys',
      'data integrity / constant collections'
    ],
    sampleAnswers: {
      te: {
        text: 'పైథాన్‌లో లిస్ట్ అంటే మ్యూటబుల్ కలెక్షన్, అంటే మనం ఎలిమెంట్స్ ని చేంజ్ చేయొచ్చు, అపెండ్ చేయొచ్చు, రిమూవ్ చేయొచ్చు. స్క్వేర్ బ్రాకెట్స్ వాడతాము. ట్యుపుల్ అంటే ఇమ్మ్యూటబుల్, అంటే ఒక్కసారి క్రియేట్ చేశాక చేంజ్ చేయలేము, పేరెంథిసిస్ వాడతాము. ట్యుపుల్స్ మెమరీ తక్కువ తీసుకుంటాయి, ఇంకా డిక్షనరీ కీస్ గా కూడా వాడొచ్చు ఎందుకంటే అవి హ్యాషబుల్.',
        romanized: 'Python lo list ante mutable collection, ante elements change cheyochu, append cheyochu. Square brackets vadathamu. Tuple ante immutable, once create chesaka change cheyalemu. Tuples memory thakkuva teesukuntaayi, dictionary keys ga kooda vadachu.',
        conceptScore: 9.5
      },
      hi: {
        text: 'पायथन में लिस्ट म्यूटेबल होती है, यानी हम डेटा को बाद में बदल सकते हैं, अपेंड या डिलीट कर सकते हैं। इसके लिए स्क्वायर ब्रैकेट्स इस्तेमाल होते हैं। टुपल इम्यूटेबल होता है, एक बार बनाने के बाद चेंज नहीं किया जा सकता। टुपल्स मेमोरी में तेज़ होते हैं और इन्हें डिक्शनरी की के रूप में भी यूज़ किया जा सकता है।',
        romanized: 'Python me list mutable hoti hai, data change kar sakte hain. Tuple immutable hota hai. Tuples memory me fast hote hain aur dictionary keys ki tarah use ho sakte hain.',
        conceptScore: 9.2
      },
      ta: {
        text: 'பைத்தானில் பட்டியல் (List) என்பது மாற்றக்கூடியது (mutable), நாம் கூறுகளை மாற்றலாம். ஆனால் டூப்பிள் (Tuple) என்பது மாற்ற முடியாதது (immutable). டூப்பிள் குறைந்த நினைவகத்தைப் பயன்படுத்துகிறது மேலும் அகராதி சாவிகளாகப் (dictionary keys) பயன்படுத்தலாம்.',
        romanized: 'Python-il list mutable, tuple immutable. Tuples memory efficient and dictionary keys-aga use pannalam.',
        conceptScore: 9.0
      },
      en_hesitant: {
        text: 'Uh, list in Python is with square brackets, and we can change values. Tuple is round bracket, and cannot change. Tuple is fast, I think.',
        fluencyScore: 5.5,
        notes: 'Understood the core point, but lacked professional terminology like "mutable/immutable data structures", "memory overhead", and "hashable keys for dictionary mapping".'
      },
      en_golden: {
        text: 'In Python, the primary distinction is mutability: lists are mutable and enclosed in square brackets, allowing runtime additions and modifications, whereas tuples are immutable and defined using parentheses. Because tuples are immutable, they have a smaller memory footprint, execute slightly faster, and are hashable, making them suitable as dictionary keys or for fixed data integrity.',
        fluencyScore: 9.8
      }
    }
  },
  {
    id: 'web-virtual-dom',
    category: 'Frontend & React',
    role: 'Frontend Engineer / React Developer',
    difficulty: 'Intermediate',
    title: 'How Virtual DOM and Reconciliation Work',
    question: {
      en: 'What is the Virtual DOM in React, and how does the reconciliation process optimize UI rendering?',
      te: 'రియాక్ట్‌లో వర్చువల్ డామ్ (Virtual DOM) అంటే ఏమిటి? రీకాన్సిలియేషన్ ప్రాసెస్ ద్వారా యూఐ రెండరింగ్ ఎలా ఆప్టిమైజ్ అవుతుంది?',
      hi: 'रिएक्ट में वर्चुअल DOM क्या है, और रीकॉन्सिलिएशन प्रक्रिया UI रेंडरिंग को कैसे ऑप्टिमाइज़ करती है?',
      ta: 'ரியாக்டில் விர்ச்சுவல் DOM என்றால் என்ன, மற்றும் ரீகான்சிலியேஷன் செயல்முறை UI ரெண்டரிங்கை எவ்வாறு மேம்படுத்துகிறது?'
    },
    expectedConcepts: [
      'in-memory representation of real DOM',
      'diffing algorithm / tree comparison',
      'batching updates',
      'minimizing expensive browser reflows & repaints',
      'keys in lists for stable identity'
    ],
    sampleAnswers: {
      te: {
        text: 'రియాక్ట్ లో వర్చువల్ డామ్ అనేది రియల్ బ్రౌజర్ డామ్ కి ఒక లైట్ వెయిట్ జావాస్క్రిప్ట్ ఆబ్జెక్ట్ కాపీ. ఏదైనా స్టేట్ చేంజ్ అయినప్పుడు, రియాక్ట్ కొత్త వర్చువల్ డామ్ ట్రీ ని క్రియేట్ చేస్తుంది. పాత ట్రీ తో కొత్త ట్రీ ని డిఫింగ్ అల్గోరిథం ద్వారా కంపేర్ చేసి, కేవలం మారిన ఎలిమెంట్స్ ని మాత్రమే రియల్ డామ్ లో అప్‌డేట్ చేస్తుంది. దీనివల్ల బ్రౌజర్ రీఫ్లోస్ మరియు రీపెయింట్స్ తగ్గి పర్ఫార్మెన్స్ చాలా పెరుగుతుంది.',
        romanized: 'React lo Virtual DOM real DOM ki lightweight JS object copy. State change ainappudu diffing algorithm tho compare chesi, only changed elements ni real DOM lo update chesthundi.',
        conceptScore: 9.8
      },
      hi: {
        text: 'वर्चुअल DOM रिएक्ट में रियल DOM का एक जावास्क्रिप्ट रिप्रेजेंटेशन है। जब भी कोई स्टेट बदलती है, तो रिएक्ट नया वर्चुअल DOM बनाकर पुराने से तुलना (Diffing) करता है और सिर्फ बदले हुए भाग को रियल DOM में बैच करके अपडेट करता है।',
        romanized: 'Virtual DOM real DOM ka JS representation hai. State change par Diffing karke sirf changed elements update karta hai.',
        conceptScore: 9.4
      },
      ta: {
        text: 'விர்ச்சுவல் DOM என்பது உண்மையான DOM இன் நினைவக நகலாகும். நிலை (state) மாறும்போது, டிஃப்பிங் (diffing) அல்காரிதம் மூலம் மாற்றங்களை மட்டும் அடையாளம் கண்டு உண்மையான DOM ஐப் புதுப்பிக்கிறது.',
        romanized: 'Virtual DOM real DOM in lightweight memory copy. Diffing algorithm changed parts mattum update pannum.',
        conceptScore: 9.1
      },
      en_hesitant: {
        text: 'Virtual DOM is like duplicate of DOM in JS. When click button, it compares and changes only that place. Real DOM is very slow, so virtual DOM is fast.',
        fluencyScore: 5.8,
        notes: 'Good intuition, but missed terms like "in-memory tree reconciliation", "batched mutations", and "browser reflow/repaint bottlenecks".'
      },
      en_golden: {
        text: 'The Virtual DOM is a lightweight in-memory representation of the actual browser DOM. When component state updates occur, React generates a new Virtual DOM tree and runs a diffing algorithm (Reconciliation) against the previous tree. It computes the minimal set of changes and batches updates to the real DOM, preventing costly browser reflows and repaints.',
        fluencyScore: 9.7
      }
    }
  },
  {
    id: 'dsa-hashmap-collisions',
    category: 'Data Structures & Algorithms',
    role: 'Software Engineer / SDE',
    difficulty: 'Intermediate',
    title: 'Hash Table Collisions and Resolution Techniques',
    question: {
      en: 'What is a collision in a Hash Table, and how do separate chaining and open addressing resolve it?',
      te: 'హాష్ టేబుల్‌లో కొలిజన్ (Collision) అంటే ఏమిటి? సెపరేట్ చైనింగ్ మరియు ఓపెన్ అడ్రెస్సింగ్ పద్ధతులు దీనిని ఎలా పరిష్కరిస్తాయి?',
      hi: 'हैश टेबल में कोलिजन क्या है, और सेपरेट चेनिंग और ओपन एड्रेसिंग इसे कैसे हल करते हैं?',
      ta: 'ஹாஷ் அட்டவணையில் மோதல் (Collision) என்றால் என்ன, அதைத் தீர்க்கும் முறைகள் யாவை?'
    },
    expectedConcepts: [
      'hash function mapping two keys to the same index',
      'separate chaining (linked lists / red-black trees at buckets)',
      'open addressing (linear probing, quadratic probing, double hashing)',
      'load factor and rehashing / resizing',
      'average O(1) vs worst-case O(n) lookup'
    ],
    sampleAnswers: {
      te: {
        text: 'హాష్ టేబుల్ లో రెండు వేర్వేరు కీస్ కి హాష్ ఫంక్షన్ ఒకే ఇండెక్స్ కాలిక్యులేట్ చేసినప్పుడు కొలిజన్ జరుగుతుంది. దీన్ని సాల్వ్ చేయడానికి రెండు మెయిన్ పద్ధతులు ఉన్నాయి. ఒకటి సెపరేట్ చైనింగ్ - ఇందులో ప్రతి బకెట్ లో లింక్డ్ లిస్ట్ పెడతాము. రెండవది ఓపెన్ అడ్రెస్సింగ్ - ఇందులో నెక్స్ట్ ఖాళీ స్లాట్ కోసం లీనియర్ లేదా క్వాడ్రాటిక్ ప్రోబింగ్ వాడతాము. లోడ్ ఫ్యాక్టర్ పెరిగితే రీహాషింగ్ చేస్తాము.',
        romanized: 'Hash table lo two different keys ki same hash index generate aithe collision antaru. Chaining lo linked list use chesthamu, Open addressing lo empty slot kosam linear probing vadathamu.',
        conceptScore: 9.6
      },
      hi: {
        text: 'जब हैश फंक्शन दो अलग-अलग कीज़ के लिए एक ही इंडेक्स देता है, तो उसे कोलिजन कहते हैं। इसे हल करने के लिए सेपरेट चेनिंग में हर स्लॉट पर लिंक्ड लिस्ट बनाते हैं, और ओपन एड्रेसिंग में प्रोबिंग के ज़रिए खाली स्लॉट ढूंढते हैं।',
        romanized: 'Collision tab hota hai jab 2 keys same hash index generate karti hain. Chaining me linked list use hoti hai, open addressing me next empty slot probe hota hai.',
        conceptScore: 9.3
      },
      ta: {
        text: 'இரண்டு வெவ்வேறு சாவிகள் ஒரே அட்டவணை குறியீட்டை (index) உருவாக்கும் போது மோதல் ஏற்படுகிறது. தனி இணைப்பு (Separate chaining) மற்றும் திறந்த முகவரியிடல் (Open addressing) மூலம் இதை சரிசெய்யலாம்.',
        romanized: 'Two keys same hash index produce pannumbodhu collision aagum. Chaining and open addressing moolam solve pannalam.',
        conceptScore: 9.0
      },
      en_hesitant: {
        text: 'Collision means two items want same box in table. To fix, we can make a list inside the box, or we look for next empty box. If full, we resize.',
        fluencyScore: 5.4,
        notes: 'Clear physical intuition, but lacked formal computer science terms: "hash function deterministic mapping", "bucket chaining", "linear/quadratic probing", and "load factor threshold".'
      },
      en_golden: {
        text: 'A collision occurs when a hash function maps two distinct keys to the same index in the underlying array. In Separate Chaining, each bucket stores a pointer to a data structure like a linked list or balanced tree to hold multiple entries. In Open Addressing, collisions are resolved by probing for alternative vacant slots using techniques like linear probing, quadratic probing, or double hashing. When the load factor exceeds a threshold, the table rehashes into a larger capacity.',
        fluencyScore: 9.9
      }
    }
  },
  {
    id: 'ds-overfitting',
    category: 'AI & Data Science',
    role: 'Machine Learning / Data Scientist',
    difficulty: 'Intermediate',
    title: 'Overfitting vs Underfitting and Regularization',
    question: {
      en: 'What is overfitting in machine learning, and what techniques do you use to detect and prevent it?',
      te: 'మెషిన్ లెర్నింగ్‌లో ఓవర్‌ఫిట్టింగ్ అంటే ఏమిటి? దానిని గుర్తించడానికి మరియు నివారించడానికి మీరు ఏ పద్ధతులను ఉపయోగిస్తారు?',
      hi: 'मशीन लर्निंग में ओवरफिटिंग क्या है, और आप इसका पता लगाने और इसे रोकने के लिए किन तकनीकों का उपयोग करते हैं?',
      ta: 'மெஷின் லேர்னிங்கில் ஓவர்ஃபிட்டிங் என்றால் என்ன, அதை எவ்வாறு தடுத்து சரிசெய்வது?'
    },
    expectedConcepts: [
      'high variance / low bias',
      'model memorizing training noise instead of general patterns',
      'train error low vs validation error high',
      'regularization (L1 Lasso, L2 Ridge, Dropout)',
      'cross-validation, early stopping, more data, data augmentation'
    ],
    sampleAnswers: {
      te: {
        text: 'ఓవర్‌ఫిట్టింగ్ అంటే మోడల్ ట్రైనింగ్ డేటాలోని నాయిస్‌ని కూడా నేర్చుకుని మెమోరైజ్ చేసుకోవడం. దీనివల్ల ట్రైనింగ్ అక్యూరసీ చాలా ఎక్కువగా ఉంటుంది కానీ టెస్ట్ లేదా వ్యాలిడేషన్ డేటాపై పర్ఫార్మెన్స్ పడిపోతుంది. దీన్ని ప్రివెంట్ చేయడానికి L1, L2 రెగ్యులరైజేషన్, న్యూరల్ నెట్‌వర్క్స్‌లో డ్రాపౌట్, క్రాస్-వ్యాలిడేషన్, ఎర్లీ స్టాపింగ్ లేదా ఇంకా ఎక్కువ డేటా యాడ్ చేయడం వంటివి చేస్తాం.',
        romanized: 'Overfitting ante model training data noise kooda memorize chesukuntundi. High training accuracy untundi kani test data lo drop avthundi. L1/L2 regularization, dropout, early stopping tho control chesthamu.',
        conceptScore: 9.7
      },
      hi: {
        text: 'ओवरफिटिंग तब होती है जब मॉडल ट्रेनिंग डेटा को याद कर लेता है और नए डेटा पर खराब परफॉर्म करता है। इसे रोकने के लिए L1/L2 रेगुलराइजेशन, ड्रॉपआउट, क्रॉस-वैलिडेशन और अर्ली स्टॉपिंग का इस्तेमाल किया जाता है।',
        romanized: 'Overfitting me model train data memorize kar leta hai. L1/L2 regularization, dropout aur early stopping se prevent karte hain.',
        conceptScore: 9.2
      },
      ta: {
        text: 'ஓவர்ஃபிட்டிங் என்பது மாடல் பயிற்சித் தரவை அதிகமாக மனப்பாடம் செய்து புதிய தரவில் தோல்வியடைவதாகும். இதைத் தடுக்க எல்1, எல்2 முறைப்படுத்தல் மற்றும் ஆரம்பத்திலேயே நிறுத்துதல் (early stopping) உதவும்.',
        romanized: 'Overfitting training data memorize pannum. L1/L2 regularization and early stopping tho prevent pannalam.',
        conceptScore: 8.9
      },
      en_hesitant: {
        text: 'Overfitting is model is too good in training, but fail in testing. It memorizes noise. We can stop early, make data bigger, or use dropout in neural network.',
        fluencyScore: 6.2,
        notes: 'Good conceptual grasp. Can be enhanced with technical precision: "generalization error", "bias-variance tradeoff", "L1/L2 penalty terms", and "k-fold cross-validation".'
      },
      en_golden: {
        text: 'Overfitting occurs when a model exhibits high variance by learning the noise and idiosyncrasies of the training data rather than underlying generalizable patterns, resulting in low training error but high validation error. We diagnose it using learning curves and cross-validation, and mitigate it using L1/L2 regularization penalties, dropout in deep architectures, early stopping, pruning, and data augmentation.',
        fluencyScore: 9.8
      }
    }
  },
  {
    id: 'hr-difficult-bug',
    category: 'HR & Behavioral',
    role: 'All Engineering Roles (STAR Method)',
    difficulty: 'Foundational',
    title: 'Explain a Difficult Technical Challenge or Bug You Solved',
    question: {
      en: 'Describe a challenging technical bug or problem you recently encountered. How did you diagnose and resolve it?',
      te: 'మీరు ఇటీవల ఎదుర్కొన్న ఒక క్లిష్టమైన టెక్నికల్ బగ్ లేదా సమస్యను వివరించండి. మీరు దానిని ఎలా విశ్లేషించి పరిష్కరించారు?',
      hi: 'हाल ही में आपके द्वारा हल किए गए किसी कठिन तकनीकी बग का वर्णन करें। आपने उसका विश्लेषण और समाधान कैसे किया?',
      ta: 'நீங்கள் சமீபத்தில் எதிர்கொண்ட கடினமான தொழில்நுட்ப சிக்கலை விவரிக்கவும். அதை எவ்வாறு சரிசெய்தீர்கள்?'
    },
    expectedConcepts: [
      'STAR method (Situation, Task, Action, Result)',
      'systematic root cause analysis / debugging tools',
      'collaboration / communication',
      'prevention / unit testing / monitoring'
    ],
    sampleAnswers: {
      te: {
        text: 'మా ప్రాజెక్ట్ ప్రొడక్షన్ లో ఒక మెమరీ లీక్ బగ్ వచ్చింది, సర్వర్ ప్రతి 3 రోజులకు క్రాష్ అయ్యేది. నేను నోడ్.జెఎస్ హీప్ స్నాప్‌షాట్స్ తీసుకుని ప్రొఫైల్ చేసాను. అప్పుడు తెలిసింది అన్‌క్లోజ్డ్ డేటాబేస్ కనెక్షన్ పూల్స్ మరియు గ్లోబల్ ఈవెంట్ లిజనర్స్ మెమరీ ని హోల్డ్ చేస్తున్నాయని. నేను కనెక్షన్ క్లీనప్ మిడిల్‌వేర్ రాసి, యూనిట్ టెస్ట్స్ యాడ్ చేసి, ప్రమోతియస్ మానిటరింగ్ అలర్ట్స్ సెట్ చేసాను. ఆ తర్వాత మెమరీ యూసేజ్ 65% తగ్గింది.',
        romanized: 'Project lo memory leak vachindi, server 3 days ki crash ayyedi. Node heap dump profile chesi connection pool leak identify chesa. Fix chesi Prometheus alerts petta, 65% memory usage thaggindi.',
        conceptScore: 9.5
      },
      hi: {
        text: 'हमारे प्रोडक्शन सर्वर में मेमोरी लीक था जिससे सर्वर क्रैश हो रहा था। मैंने हीप डंप्स का विश्लेषण किया और पाया कि अनक्लोज्ड डीबी कनेक्शंस जिम्मेदार थे। मैंने कनेक्शन पूल फिक्स किया और ऑटोमेटेड टेस्ट्स जोड़े जिससे 65% मेमोरी घटी।',
        romanized: 'Production me memory leak tha. Heap dumps analyze karke connection leak pakda aur fix kiya.',
        conceptScore: 9.1
      },
      ta: {
        text: 'எங்கள் தயாரிப்பில் நினைவகக் கசிவு (memory leak) இருந்தது. நான் ஹீப் டம்ப்களை ஆய்வு செய்து தரவுத்தள இணைப்பு சிக்கலைக் கண்டறிந்து சரிசெய்தேன். 65% நினைவகப் பயன்பாடு குறைந்தது.',
        romanized: 'Production la memory leak irundhadhu. Heap dump inspect panni connection leak fix pannen.',
        conceptScore: 9.0
      },
      en_hesitant: {
        text: 'In my project server crashed because memory problem. I saw heap dump and found database connection was not closed properly. I fixed the code and added tests. Then server worked fine.',
        fluencyScore: 6.0,
        notes: 'Good direct answer. Improved version frames this using executive impact, metrics, and structured STAR storytelling.'
      },
      en_golden: {
        text: 'In our production environment, we observed progressive memory bloat causing service restarts every 72 hours. I took diagnostic heap snapshots and profiled allocations, identifying uncollected database connection listeners in an asynchronous middleware pipeline. I refactored the connection lifecycle management, implemented automated leak regression tests, and set up Prometheus alert thresholds, which reduced steady-state memory consumption by 65%.',
        fluencyScore: 9.8
      }
    }
  }
];

function getQuestions() {
  return QUESTION_BANK;
}

function getQuestionById(id) {
  return QUESTION_BANK.find(q => q.id === id) || QUESTION_BANK[0];
}

module.exports = {
  QUESTION_BANK,
  getQuestions,
  getQuestionById
};
