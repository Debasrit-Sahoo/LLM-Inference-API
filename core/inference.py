from transformers import AutoTokenizer, AutoModelForCausalLM
import torch 
from config import settings
from huggingface_hub import login

login(token=settings.huggingface_token)

device = "cpu" if settings.force_cpu else ("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(settings.model_name)
model = AutoModelForCausalLM.from_pretrained(
    settings.model_name,
    dtype=torch.float16,
    device_map="auto"
    )

def run_inference(message: str) -> str:
    prompt = f"<s>[INST] {message} [/INST]"

    encoded = tokenizer(
        prompt,
        return_tensors="pt",
        return_attention_mask = True
    )

    inputs = encoded["input_ids"].to(model.device)
    attention_mask = encoded["attention_mask"].to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            inputs,
            attention_mask = attention_mask,
            max_new_tokens = settings.max_new_tokens,
            pad_token_id = tokenizer.eos_token_id,
            do_sample = True,
            temperature=settings.temperature,
            top_p=settings.top_p,
        )
    
    response_ids = output_ids[:, inputs.shape[-1]:]
    return tokenizer.decode(response_ids[0], skip_special_tokens = True)