# -*- coding: utf-8 -*-
"""keyphrase-extraction.ipynb

Automatically generated by Colaboratory.

Original file is located at
https://colab.research.google.com/drive/18kk0A7G6Rnza19JcjPSPkuWniyqNtkxl
"""

# Install required packages
!pip install transformers
!pip install datasets

from datasets import load_dataset, Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments, DataCollatorForTokenClassification
import numpy as np
import datasets

# Labels
label_list = ["B", "I", "O"]
lbl2idx = {"B": 0, "I": 1, "O": 2}
idx2label = {0: "B", 1: "I", 2: "O"}

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
max_length = 512

# Dataset parameters
dataset_full_name = "midas/inspec"
dataset_subset = "raw"
dataset_document_column = "document"
dataset_biotags_column = "doc_bio_tags"

def preprocess_function(all_samples_per_split):
    tokenized_samples = tokenizer.batch_encode_plus(
        all_samples_per_split[dataset_document_column],
        padding="max_length",
        truncation=True,
        is_split_into_words=True,
        max_length=max_length,
    )
    total_adjusted_labels = []

    for k in range(0, len(tokenized_samples["input_ids"])):
        prev_wid = -1
        word_ids_list = tokenized_samples.word_ids(batch_index=k)
        existing_label_ids = all_samples_per_split[dataset_biotags_column][k]
        i = -1
        adjusted_label_ids = []

        for wid in word_ids_list:
            if wid is None:
                adjusted_label_ids.append(lbl2idx["O"])
            elif wid != prev_wid:
                i += 1
                adjusted_label_ids.append(lbl2idx[existing_label_ids[i]])
                prev_wid = wid
            else:
                adjusted_label_ids.append(lbl2idx[f"{'I' if existing_label_ids[i] == 'B' else existing_label_ids[i]}"])

        total_adjusted_labels.append(adjusted_label_ids)

    tokenized_samples["labels"] = total_adjusted_labels
    return tokenized_samples

# Load dataset
dataset = load_dataset(dataset_full_name, dataset_subset)

# Preprocess dataset
tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Explore just a subset of the dataset
train_data = tokenized_dataset['train'][:5]
validation_data = tokenized_dataset['validation'][:2]
test_data = tokenized_dataset['test'][:2]

# Create Dataset objects for each split
train_dataset = Dataset.from_dict(train_data)
test_dataset = Dataset.from_dict(test_data)
validation_dataset = Dataset.from_dict(validation_data)

# Create a DatasetDict by combining the datasets
dataset_dict = DatasetDict({
    'train': train_dataset,
    'test': test_dataset,
    'validation': validation_dataset
})

# Define custom evaluation metrics
accuracy = datasets.load_metric("accuracy")
f1_metric = datasets.load_metric("f1")

def my_compute_metrics(eval_pred):
    logits, labels = eval_pred
    refs = labels.flatten()
    predictions = np.argmax(logits, axis=-1)
    pred = predictions.flatten()
    return {
        "accuracy": accuracy.compute(predictions=pred, references=refs)["accuracy"],
        "f1_micro": f1_metric.compute(predictions=pred, references=refs, average="micro")["f1"],
        "f1_macro": f1_metric.compute(predictions=pred, references=refs, average="macro")["f1"],
    }

# Load pretrained model
model_name = 'ml6team/keyphrase-extraction-distilbert-inspec'
# model_name = 'ml6team/keyphrase-extraction-kbir-semeval2017'
# model_name = 'ml6team/keyphrase-extraction-kbir-inspec'
# model_name = 'Voicelab/vlt5-base-keywords'
model = AutoModelForTokenClassification.from_pretrained(model_name)

# Define training arguments
training_args = TrainingArguments(
    output_dir="/content/drive/MyDrive/thesis",
    overwrite_output_dir=True,
    num_train_epochs=5,
    per_device_train_batch_size=8,
    save_steps=100,
    evaluation_strategy="steps",
    eval_steps=100,
    learning_rate=1e-4,
)

# Create Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=None,
    train_dataset=dataset_dict['train'],
    eval_dataset=dataset_dict['validation'],
    compute_metrics=my_compute_metrics,
)

# Fine-tune the model
trainer.train()

# Evaluate on the validation set
print(trainer.evaluate())

# Predict on the test data
prediction = trainer.predict(dataset_dict['test'])

# Get predicted logits, predicted labels, and true labels
predicted_logits = prediction.predictions
predicted_labels = np.argmax(predicted_logits, axis=-1)
true_labels = prediction.label_ids

# Example of the first 5 tokens' ground true labels and their predicted logits
print(predicted_logits[0][:1])
print(predicted_labels[0][100:105])
print(true_labels[0][100:105])