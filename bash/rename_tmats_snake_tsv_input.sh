awk -F"\t" '{for(i=1;i<=NF;i++){printf("mv Cycle_1_F%03d_tmat.npy Cycle_1_F%03d_tmat_%03d_%03d.npy\n", $i,$i,i-1,NR-1)}}' wells_snake.tsv
