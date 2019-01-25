library(deepSNV, quietly=TRUE)

args = commandArgs(trailingOnly=TRUE)
# expect bam_dir, region, number of cores, outfile

regions <- read.table(args[2], header=FALSE)
names(regions) <- c('chr','start','end')
regions <- with(regions, GRanges(chr, IRanges(start, end)))

files <- dir(args[1], pattern="*.bam$", full.names=TRUE)
MC_CORES <- args[3]

counts <- loadAllData(files, regions, mc.cores=MC_CORES)
BF <- mcChunk("bbb", split = 200, counts, mc.cores=MC_CORES)
vcf <- bf2Vcf(BF=BF, counts=counts, regions=regions)
writeVcf(vcf, args[4])
