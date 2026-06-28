#!/bin/bash

echo -e "\033[1;34m==================================================\033[0m"
echo -e "\033[1;34m[SHA Hash-chain] FIRST FIVE ROWS of the Table! \033[0m"
echo -e "\033[1;34mBnechmarking a Tree with 2**13 Leaves !\033[0m"
echo -e "\033[1;34mReproducing Table 6: First set of rows (around 7~9 min) \033[0m"
echo -e "\033[1;34m==================================================\033[0m"

provenview --circuit circuits/merkle_fold_step_sha_16.r1cs --function vector_commitment --input samples/16-subtree/ --output folding-proof-file.json --witnessgenerator circuits/merkle_fold_step_sha_16_cpp/merkle_fold_step_sha_16 --synthetic 512

echo -e "\033[1;34m==================================================\033[0m"
echo -e "\033[1;34m[POSEIDON Hash-chain] SECOND FOUR ROWS of the Table! \033[0m"
echo -e "\033[1;34mBnechmarking a Tree with 2**15 Leaves!\033[0m"
echo -e "\033[1;34mReproducing Table 6: first row results (around 1~2 min) \033[0m"
echo -e "\033[1;34m==================================================\033[0m"

provenview --circuit circuits/merkle_fold_step_128.r1cs --function vector_commitment --input samples/128-subtree/ --output folding-proof-file.json --witnessgenerator circuits/merkle_fold_step_128_cpp/merkle_fold_step_128

echo -e "\033[1;34m==================================================\033[0m"
echo -e "\033[1;34mBnechmarking a Tree with 2**20 Leaves!\033[0m"
echo -e "\033[1;34mReproducing Table 6: LAST row results (around 30~40 min) \033[0m"
echo -e "\033[1;34m==================================================\033[0m"

provenview --circuit circuits/merkle_fold_step_256.r1cs --function vector_commitment --input samples/256-subtree/ --output folding-proof-file.json --witnessgenerator circuits/merkle_fold_step_256_cpp/merkle_fold_step_256 --synthetic 4096
