library(ComplexHeatmap)
library(circlize)
library("tidyverse")
library(vegan)
library("factoextra")
library(RColorBrewer)
library("FactoMineR")
library("RColorBrewer")
display.brewer.all(colorblindFriendly = TRUE)


fig <- function(width, heigth){
     options(repr.plot.width = width, repr.plot.height = heigth)}

dataPA <- read.csv("cazymes_PA_metadata_FS.csv", header=T, row.names="Assembly.accession")

library(dplyr)
data_matrixPA <- dataPA[ , !names(dataPA) %in% c("orfs", "index","Genus", "Family", "Genome")]

tib <- data_matrixPA %>%
    group_by(Origin) %>%
    summarise_all("mean")%>%

data_matrix_transposePA <- t(tib)
data_matrix_transposePA <- as.matrix(data_matrix_transposePA)
colnames(data_matrix_transposePA) <- data_matrix_transposePA[1,]
data_matrix_transposePA <- data_matrix_transposePA[-1, ] 


svg(file="heatmap.svg")

#largura, altura:
fig(8, 8)
set.seed(40)


mycol <- rev(colorRampPalette(brewer.pal(9, "RdBu"))(20))

hmap <- Heatmap(as.matrix(data_matrix_transposePA),
                name = "Mean Presence per Origin",
                col = mycol,
                border=TRUE,
    rect_gp = gpar(col = "white", lwd = 0.2),
                
    heatmap_width = unit(9, "cm"), 
    heatmap_height = unit(9, "cm"),
    
    #use_raster = TRUE, 
    #raster_device = "png",   
    #raster_by_magick = TRUE,

    row_km = 4, row_km_repeats = 100,
    column_km = 1, column_km_repeats = 100,
                               
   # column_title = "Origin", 
    #column_title_side = "top",  
    #column_title_gp=gpar(fontsize = 8, fontface = "bold"),
    
    column_names_rot = 1,
    column_names_side="top",
    column_names_gp = gpar(fontsize = 8, fontface="bold"), 
    column_names_centered = TRUE,
                
    row_title = "CAZymes", 
    row_title_side="left",
    row_title_gp=gpar(fontsize = 8, fontface = "bold"),                  
    
    row_names_gp = gpar(fontsize = 6),
    
    show_row_names = TRUE,
    show_column_names = TRUE,
                
    cluster_rows = TRUE,
    cluster_columns = TRUE, show_column_dend = FALSE, 
    
    heatmap_legend_param = list(title_gp = gpar(fontsize = 8, fontface = "bold" ), labels_gp = gpar(fontsize = 8),
                               direction = "horizontal", legend_width = unit(3.5, "cm")))#, labels = c("0%","",""  ,"100%")) #"50%
                                

draw(hmap,  heatmap_legend_side = "bottom") # merge_legend = FALSE, heatmap_legend_side = "bottom", annotation_legend_side = "right"

dev.off()

