from transformers import T5ForConditionalGeneration, T5TokenizerFast

t5_model = T5ForConditionalGeneration.from_pretrained("ThomasSimonini/t5-end2end-question-generation")

tokenizer = T5TokenizerFast.from_pretrained("t5-large")

def get_questions(input_string, **generator_args):
    generator_args = {
    "max_length": 256,
    "num_beams": 10,
    "length_penalty": 1.5,
    "no_repeat_ngram_size": 1,
    "early_stopping": True,
    }
    input_string = "generate questions: " + input_string + " </s>"
    input_ids = tokenizer.encode(input_string, return_tensors="pt")
    res = t5_model.generate(input_ids, **generator_args)
    output = tokenizer.batch_decode(res, skip_special_tokens=True)
    output = [item.split("<sep>") for item in output]
    return output