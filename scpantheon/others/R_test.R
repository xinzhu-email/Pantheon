# install.packages("vscDebugger", dependencies=TRUE, repos = "https://mirrors.sustech.edu.cn/CRAN/")



library(Seurat)
library(Matrix)
library(cowplot)
library(dplyr)

read_mtx <- function(mtx_folder){
  sp_matrix_read <- readMM(file.path(mtx_folder,"matrix.mtx.gz")) 
  features = read.table(file.path(mtx_folder,"features.tsv.gz"))
  # head(features)
  # write.table(features, "features.txt", sep = "\t", quote = FALSE, row.names = FALSE)
  barcodes = read.table(file.path(mtx_folder,"barcodes.tsv.gz"))
  if(ncol(features)>1){
    sp_matrix_read@Dimnames[[1]] = features[,2] # row name
  }else{
    sp_matrix_read@Dimnames[[1]] = features[,1] # row name
  }
  sp_matrix_read@Dimnames[[2]] = barcodes[,1] # col name
  return(sp_matrix_read)
}


counts <- read_mtx('C:/Users/23606/Documents/Workspace/Pantheon/scpantheon/others/data/RNA_simulator_3_3')
data <- CreateSeuratObject(counts = counts, assay='RNA')
data.adt <- as.sparse(t(read.csv(file = 'C:/Users/23606/Documents/Workspace/Pantheon/scpantheon/others/data/simulator_out/ADT_simulator_3_3.csv', sep = ",",header = TRUE, row.names = 1)))
data.adt <- CreateAssayObject(counts = data.adt)
data[['ADT']] <- data.adt
label <- read.csv('C:/Users/23606/Documents/Workspace/Pantheon/scpantheon/others/data/simulator_out/droplets_composition_3_3.csv')
data@meta.data['label'] <- label[,'cell_type'] # data frame 行对应于数据集中的细胞或样本，列对应于元数据的不同属性

DefaultAssay(data) <- 'RNA'
data <- NormalizeData(data) %>% FindVariableFeatures() %>% ScaleData() %>% RunPCA() # 归一化、筛选变异特征、尺度化和运行PCA降维
DefaultAssay(data) <- 'ADT'
VariableFeatures(data) <- rownames(data[["ADT"]])
# CLR（细胞内部相对标准化）归一化、尺度化和运行PCA降维
data <- NormalizeData(data, normalization.method = 'CLR', margin = 2) %>% ScaleData() %>% RunPCA(reduction.name = 'apca')
# 降维数据计算多模态邻居
data <- FindMultiModalNeighbors(data, reduction.list = list("pca", "apca"), dims.list = list(1:30, 1:18), modality.weight.name = "RNA.weight")
# WSNN算法细胞聚类
data <- FindClusters(data, graph.name = "wsnn", algorithm = 3, resolution = 1, verbose = FALSE)

# 权重相似图计算UMAP降维
data <- RunUMAP(data, nn.name = "weighted.nn", reduction.name = "wnn.umap", reduction.key = "wnnUMAP_")
p1 <- DimPlot(data, reduction = 'wnn.umap', label = TRUE, repel = TRUE, label.size = 2.5) + NoLegend()
p2 <- DimPlot(data, reduction = 'wnn.umap', group.by='label', label = TRUE, repel = TRUE, label.size = 2.5) + NoLegend()
p1+p2

# VlnPlot(data, features = "RNA.weight", group.by = 'label', sort = TRUE, pt.size = 0.1) + NoLegend()

data <- RunUMAP(data, reduction = 'pca', dims = 1:30, assay = 'RNA', reduction.name = 'rna.umap', reduction.key = 'rnaUMAP_')
p3 <- DimPlot(data, reduction = 'rna.umap', label = TRUE, repel = TRUE, label.size = 2.5) + NoLegend()
p4 <- DimPlot(data, reduction = 'rna.umap', group.by='label', label = TRUE, repel = TRUE, label.size = 2.5) + NoLegend()
p3 + p4


data <- RunUMAP(data, reduction = 'apca', dims = 1:18, assay = 'ADT', reduction.name = 'adt.umap', reduction.key = 'adtUMAP_')
p5 <- DimPlot(data, reduction = 'adt.umap', label = TRUE, repel = TRUE, label.size = 2.5) + NoLegend()
p6 <- DimPlot(data, reduction = 'adt.umap', group.by='label', label = TRUE, repel = TRUE, label.size = 2.5) + NoLegend()
p5 + p6


png(filename = "p1_p2.png", width = 10, height = 6, units = "in", res = 300)
print(plot_grid(p1, p2, ncol = 2))
dev.off()
png(filename = "p5_p6.png", width = 10, height = 6, units = "in", res = 300)
print(plot_grid(p5, p6, ncol = 2))
dev.off()
png(filename = "p3_p4.png", width = 10, height = 6, units = "in", res = 300)
print(plot_grid(p3, p4, ncol = 2))
dev.off()







  