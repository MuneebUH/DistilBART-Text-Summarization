import os
from textSummarizer.logging import logger
from transformers import AutoTokenizer
from datasets import load_dataset
from textSummarizer.entity import DataTransformationConfig

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)

    def convert_examples_to_features(self, example_batch):
        # Tokenize the input text (email) and target text (summary)
        input_encodings = self.tokenizer(example_batch['Email'], max_length=1024, truncation=True, padding='max_length')
        
        with self.tokenizer.as_target_tokenizer():
            target_encodings = self.tokenizer(example_batch['Summary'], max_length=128, truncation=True, padding='max_length')

        # Return the tokenized data
        return {
            'input_ids': input_encodings['input_ids'],
            'attention_mask': input_encodings['attention_mask'],
            'labels': target_encodings['input_ids']
        }

    def convert(self):
        # Load the dataset directly from CSV files using `load_dataset`
        dataset = load_dataset('csv', data_files={
            'train': os.path.join(self.config.data_path, 'train/train.csv'),
            'test': os.path.join(self.config.data_path, 'test/test.csv'),
            'val': os.path.join(self.config.data_path, 'val/val.csv')
        })

        # Apply tokenization to the dataset
        dataset = dataset.map(self.convert_examples_to_features, batched=True)

        # Save the transformed dataset to disk
        dataset.save_to_disk(os.path.join(self.config.root_dir, 'email_data_transformed'))

        logger.info(f"Dataset transformed and saved to {os.path.join(self.config.root_dir, 'email_data_transformed')}")
