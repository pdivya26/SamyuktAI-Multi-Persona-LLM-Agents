# SamyuktAI: A Hybrid Multi-Persona LLM Agent System

A domain-specialized conversational AI system with dedicated agents for **Healthcare** and **Legal** assistance, built using a hybrid deployment architecture combining local fine-tuning and API-based inference.

## Overview

Most LLM systems use a single general-purpose model for all queries. This works for broad knowledge tasks but fails in safety-critical domains like healthcare and law, where domain accuracy, controlled responses, and transparency are non-negotiable.

SamyuktAI addresses this by deploying two dedicated domain-specialized agents under explicit user-controlled persona management — no hidden routing, no automated intent classification.

## System Architecture

<img width="929" height="516" alt="Multi Persona LLM Agent System Architecture" src="https://github.com/user-attachments/assets/085b7e61-da19-4bf7-a816-ee1f82b44840" />

### Key Design Decisions

- **No Automated Query Routing**: Users explicitly select their domain before querying. This ensures transparency, predictability, and prevents misclassification in safety-critical scenarios.
- **Hybrid Deployment**: Healthcare agent is locally hosted (fine-tuned); Legal agent uses Groq API with prompt-based domain conditioning. This balances infrastructure efficiency with domain specialization.
- **Session-Level Persona Isolation**: Each session is locked to one domain, preventing cross-domain reasoning interference.

## Agents

### Healthcare Agent
- **Base Model**: OpenLLaMA 7B V2
- **Fine-tuning Method**: QLoRA (Quantized Low-Rank Adaptation) with 4-bit quantization
- **Training Data**: MedQuAD — Medical Question Answering Dataset (patient-oriented clinical knowledge)
- **Behavior**: Provides general health information, symptom explanations, and preventive care guidance. Does not make diagnostic or prescriptive decisions.
- **Deployment**: Locally hosted

Model weights are not included in this repository due to file size. To reproduce, run the training notebook with the MedQuAD dataset.

### Legal Agent
- **Base**: Hosted LLM via Groq API
- **Domain Alignment**: Structured system prompts and persona instruction templates
- **Behavior**: Provides legal information, explains Indian legal procedures, and responds in structured legal terminology. Does not provide specific legal advice.
- **Deployment**: API-based (no local fine-tuning required)

## Tech Stack

| Component | Technology |
|---|---|
| Healthcare Agent | OpenLLaMA 7B V2, QLoRA, PEFT, Hugging Face Transformers |
| Legal Agent | Groq API |
| Fine-tuning | QLoRA (4-bit quantization, gradient accumulation) |
| Training Data | MedQuAD Dataset |
| Frontend | HTML, CSS, JavaScript |
| Backend | Python |

## Evaluation Results

Evaluated using a structured human-in-the-loop framework with 3 independent reviewers across 40 domain-specific prompts (20 Healthcare + 20 Legal).

| Domain | Domain Relevance | Factual Correctness | Ease of Understanding |
|---|---|---|---|
| Healthcare | 100% | 89.82% | 88.77% |
| Legal | 100% | 93.33% | 92.34% |

**Evaluation Dimensions:**
- **Domain Relevance**: Whether response strictly adhered to the selected persona (binary 0/1)
- **Factual Correctness**: Accuracy of information (1–5 scale)
- **Ease of Understanding**: Clarity for non-expert users (1–5 scale)

## Fine-Tuning Details

| Parameter | Value |
|---|---|
| Base Model | OpenLLaMA 7B V2 |
| Fine-tuning Method | QLoRA |
| Quantization | 4-bit |
| Dataset | MedQuAD |
| Training Approach | Full dataset exposure for maximum domain coverage |
| Learning Rate Schedule | Constant |
| Optimization | Gradient accumulation for virtual large batch sizes |

## Project Structure

```
SamyuktAI-Multi-Persona LLM Agents/
│
├── Python Scripts/
│   ├── Multi_Persona_LLM_Agents_Training_&_Testing.ipynb   # QLoRA fine-tuning and model testing
│   └── SamyuktAI_Backend_Connection.ipynb                  # Backend integration and inference testing
│
├── SamyuktAI Web Interface/
│   ├── app.py                          # Flask backend server
│   ├── templates/
│   │   ├── homepage.html               # Main chat interface with persona selector
│   │   ├── login.html
│   │   └── register.html
│   └── static/
│       ├── style.css                   # Main interface styles
│       ├── login.css
│       └── register.css
│
├── SamyuktAI Screenshots/
│   ├── Multi Persona LLM Agent System Architecture.png
│   ├── SamyuktAI Home Page.jpeg
│   ├── SamyuktAI Medical Model.jpeg
│   └── SamyuktAI Legal Model.jpeg
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Implementation Screenshots

<img width="1919" height="866" alt="SamyuktAI Medical Model I" src="https://github.com/user-attachments/assets/4481b156-dc89-441a-8b05-a665b9cf4526" />
<img width="1916" height="865" alt="SamyuktAI Medical Model II" src="https://github.com/user-attachments/assets/f4da00db-b7c8-4acd-b4cd-def5b250981f" />
<img width="1919" height="862" alt="SamyuktAI Legal Model I" src="https://github.com/user-attachments/assets/e4eeb968-2c11-47fb-971e-24fb8afcb703" />
<img width="1919" height="862" alt="SamyuktAI Legal Model II" src="https://github.com/user-attachments/assets/55eebdae-e59e-456e-b446-73861d70040d" />

## Limitations

- Currently supports two domains (Healthcare and Legal); expanding requires new domain-specific data and fine-tuning
- Users must correctly identify which domain their query belongs to; ambiguous queries may result in suboptimal responses
- Multi-domain queries (e.g., medical insurance policies) are not natively handled
- No formal uncertainty estimation or confidence scoring
- Inference speed on the healthcare agent is hardware-dependent due to 7B model size
- Domain-specific agents may occasionally generate factually inaccurate, incomplete, or hallucinated responses due to limitations of fine-tuned language models and training data coverage.

## Future Work

- Add domain agents for Finance, Education, and Public Policy
- Introduce optional user-enabled cross-domain support (sequential agent activation)
- Transition Legal agent from API-based to fully self-hosted fine-tuned model
- Implement standardized train-test splits and automated evaluation benchmarks
- Apply model compression and distillation to reduce inference latency
- Add uncertainty-aware response generation for safety-critical applications

## Acknowledgements

- Vidyalankar Institute of Technology for infrastructure and academic support
- MedQuAD dataset contributors
- Groq for API access
- Hugging Face for open-source model weights and PEFT library

## License

This project is for academic and research purposes.
