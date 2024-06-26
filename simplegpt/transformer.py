import torch
from torch import Tensor
from torch.nn import init, Module, Embedding, ModuleList, Dropout, LayerNorm

from simplegpt.config.config import EMBED_DIM, DROPOUT_PROB, NUM_TRANSFORMER_BLOCKS, STD
from simplegpt.transformerblock import TransformerBlock


class Transformer(Module):
    def __init__(self, vocab_size: int, max_seq_len: int):
        super().__init__()
        self.token_embedding_weights = Embedding(vocab_size, EMBED_DIM)
        init.normal_(self.token_embedding_weights.weight, std=STD)

        self.position_embedding_weights = Embedding(max_seq_len, EMBED_DIM)
        init.normal_(self.position_embedding_weights.weight, std=STD)

        self.dropout = Dropout(DROPOUT_PROB)
        self.transformer_blocks = ModuleList([TransformerBlock(max_seq_len) for _ in range(NUM_TRANSFORMER_BLOCKS)])

        self.layer_norm_feedforward = LayerNorm(EMBED_DIM)
        init.zeros_(self.layer_norm_feedforward.bias)
        init.ones_(self.layer_norm_feedforward.weight)

    def forward(self, inputs: Tensor) -> Tensor:
        _, seq_len = inputs.size()
        position = torch.arange(0, seq_len).unsqueeze(0)
        position_embeddings = self.position_embedding_weights.forward(position)

        token_embeddings = self.token_embedding_weights.forward(inputs)
        block_outputs = self.dropout.forward(token_embeddings + position_embeddings)
        for transformer_block in self.transformer_blocks:
            block_outputs = transformer_block.forward(block_outputs)
        return self.layer_norm_feedforward.forward(block_outputs)
