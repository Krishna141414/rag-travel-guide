# Evaluation results

Top-k = 3, threshold = 0.5, LLM = Qwen/Qwen2.5-0.5B-Instruct on CPU.

| Metric | Result |
|---|---|
| Retrieval hit (expected article in top-3) | 7/7 |
| Answerable questions answered | 7/7 |
| Unanswerable correctly refused ("not found") | 3/3 |
| Answers where the LLM wrote its own citation | 1/7 |
| Avg response time (all) | 2.34 s |
| Avg time, answered (LLM called) | 3.34 s |
| Avg time, refused below threshold (no LLM) | 0.01 s |

| Question | Expected | Top sources | Best score | Status | OK | Time |
|---|---|---|---|---|---|---|
| Which emperor built the Taj Mahal? | Agra | Agra, Agra, Agra | 0.683 | answered | yes | 2.49 s |
| What can you see in Kaziranga National Park? | Kaziranga National Park | Kaziranga National Park, Kaziranga National Park, Kaziranga National Park | 0.673 | answered | yes | 4.2 s |
| Why is Rishikesh called the yoga capital of the world? | Rishikesh | Rishikesh, Rishikesh, Rishikesh | 0.730 | answered | yes | 4.33 s |
| When did Goa become part of India? | Goa | Goa, Goa, Goa | 0.655 | answered | yes | 2.33 s |
| What is the Golden Temple in Amritsar? | Amritsar | Amritsar, Amritsar, Varanasi | 0.713 | answered | yes | 3.74 s |
| What are the Ajanta Caves known for? | Ajanta Caves | Ajanta Caves, Ajanta Caves, Ajanta Caves | 0.774 | answered | yes | 4.49 s |
| Which city has a famous palace lit up during Dasara? | Mysore | Mysore, Mysore, Mysore | 0.624 | answered | yes | 1.81 s |
| What is the capital of Brazil? | (not in documents) | Goa, Goa, Goa | 0.473 | not_found | yes | 0.01 s |
| Who is the current CEO of Tesla? | (not in documents) | Jaipur, Jaipur, Alappuzha | 0.316 | not_found | yes | 0.01 s |
| How tall is Mount Everest? | (not in documents) | Gangtok, Darjeeling, Darjeeling | 0.493 | not_found | yes | 0.01 s |

## Answers

- **Which emperor built the Taj Mahal?** Shah Jahan built the Taj Mahal [2]*.
- **What can you see in Kaziranga National Park?** Visitors can observe various wildlife species such as Indian rhinoceros, Asian elephant, wild water buffalo, swamp deer, tiger, and fishing cat [3]*.
- **Why is Rishikesh called the yoga capital of the world?** The city hosts the International Yoga Festival annually on the first week of March since 1999, giving it the nickname of Yoga Capital of the World [1]*.
- **When did Goa become part of India?** December 1961 [2]
- **What is the Golden Temple in Amritsar?** The Golden Temple in Amritsar is the holiest site and most-visited gurudwara in Sikhism [1]*.
- **What are the Ajanta Caves known for?** The Ajanta Caves are renowned for their masterpieces of Buddhist religious art, including exquisite paintings and rock-cut sculptures that depict scenes of emotion through gesture, pose, and form [1]*.
- **Which city has a famous palace lit up during Dasara?** Mysore [1]*
- **What is the capital of Brazil?** I couldn't find this in the travel guide documents.
- **Who is the current CEO of Tesla?** I couldn't find this in the travel guide documents.
- **How tall is Mount Everest?** I couldn't find this in the travel guide documents.

`[n]*` = citation added automatically by word overlap because the model left that sentence uncited.
