import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset, load_metric

# 1. 加载数据集
dataset = load_dataset('squad')  # 使用 squad 数据集作为示例

# 2. 加载预训练模型和分词器
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 3. 数据预处理
def preprocess_function(examples):
    return tokenizer(examples['text'], truncation=True, padding='max_length', max_length=512)

encoded_dataset = dataset.map(preprocess_function, batched=True)

# 4. 划分训练集和验证集
train_dataset = encoded_dataset['train'].shuffle(seed=42).select(range(1000))  # 选择前1000个样本作为训练集
eval_dataset = encoded_dataset['test'].shuffle(seed=42).select(range(100))    # 选择前100个样本作为验证集

# 5. 定义训练参数
training_args = TrainingArguments(
    output_dir='./results',          # 输出目录
    evaluation_strategy="epoch",     # 每个 epoch 结束后进行评估
    learning_rate=2e-5,              # 学习率
    per_device_train_batch_size=8,   # 每个设备的训练批处理大小
    per_device_eval_batch_size=8,    # 每个设备的评估批处理大小
    num_train_epochs=3,              # 训练轮数
    weight_decay=0.01,               # 权重衰减
    max_grad_norm=1.0,               # 最大梯度范数
    gradient_accumulation_steps=2,   # 梯度累积步数
    warmup_steps=500,                # 学习率预热步数
    logging_dir='./logs',            # 日志目录
    logging_steps=10,                # 每10步记录一次日志
    save_steps=500,                  # 每500步保存一次模型
    save_total_limit=2,              # 最多保存2个模型
    fp16=True,                       # 使用混合精度训练
    load_best_model_at_end=True,     # 训练结束后加载最佳模型
    metric_for_best_model="accuracy",# 用于选择最佳模型的指标
    greater_is_better=True,          # 指标越大越好
)

# 6. 定义评估函数
metric = load_metric("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = torch.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

# 7. 定义 Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# 8. 开始训练
trainer.train()

# 9. 保存模型
trainer.save_model('./final_model')