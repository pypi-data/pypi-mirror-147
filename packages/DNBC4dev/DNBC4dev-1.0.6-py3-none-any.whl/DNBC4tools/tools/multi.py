import os
#from .utils import start_print_cmd
from DNBC4tools.__init__ import _root_dir

class Multi_list:
    def __init__(self, args):
        self.list = args.list
        self.starIndexDir = args.starIndexDir
        self.gtf = args.gtf

        self.outdir = args.outdir
        self.thread = args.thread
        self.cDNAconfig = args.cDNAconfig
        self.oligoconfig = args.oligoconfig
        self.oligotype = args.oligotype
        self.expectNum = args.expectNum
        self.process = args.process
        self.nosecondary = args.nosecondary
        self.include_introns = args.include_introns
        self.no_bam = args.no_bam
        self.mixseq = args.mixseq
    
    def run(self):
        with open(self.list) as samplelist:
            for line in samplelist:
                lst = line.strip().split('\t')
                name = lst[0]
                cDNAr1 = lst[1].split(';')[0]
                cDNAr2 = lst[1].split(';')[-1]
                oligor1 = lst[2].split(';')[0]
                oligor2 = lst[2].split(';')[-1]
                species = lst[-1]
                shelllist = open('%s.shell'%name,'w')
                path = '/'.join(str(_root_dir).split('/')[0:-4])+ '/bin'
                cmd_line = ['%s/DNBC4tools run --name %s --cDNAfastq1 %s --cDNAfastq2 %s --oligofastq1 %s --oligofastq2 %s --starIndexDir %s --gtf %s --species %s'
                %(path,name,cDNAr1,cDNAr2,oligor1,oligor2,self.starIndexDir,self.gtf,species)]
                if self.thread:
                    cmd_line += ['--thread %s'%self.thread]
                if self.outdir:
                    cmd_line += ['--outdir %s'%self.outdir]
                if self.cDNAconfig:
                    cmd_line += ['--cDNAconfig %s'%self.cDNAconfig]
                if self.oligoconfig:
                    cmd_line += ['--oligoconfig %s'%self.oligoconfig]
                if self.oligotype:
                    cmd_line += ['--oligotype %s'%self.oligotype]
                if self.expectNum:
                    cmd_line += ['--expectNum %s'%self.expectNum]
                if self.process:
                    cmd_line += ['--process %s'%self.process]
                if self.nosecondary:
                    cmd_line += ['--nosecondary']
                if self.include_introns:
                    cmd_line += ['--include_introns']
                if self.no_bam:
                    cmd_line += ['--no_bam']
                if self.mixseq:
                    cmd_line += ['--mixseq']               
                #cmd_line += ['--dry']
                cmd_line = ' '.join(cmd_line)
                shelllist.write(cmd_line)
                
def multi(args):
    Multi_list(args).run()

def parse_multi(parser):
    parser.add_argument('--list', metavar='FILE',help='sample list', type=str)
    parser.add_argument('--starIndexDir',type=str, metavar='PATH',help='Star index dir path.',required=True)
    parser.add_argument('--gtf',type=str, metavar='GTF',help='GTF file.')
    parser.add_argument('--outdir', metavar='PATH',help='output dir, [default is current directory].')
    parser.add_argument('--thread',type=int, metavar='INT',help='Analysis threads, [defult is 4].')
    parser.add_argument('--cDNAconfig', metavar='JASON',help='whitelist file in JSON format for cDNA fastq, the value of cell barcode is an array in the JSON, [ defalut is %s/config/DNBelabC4_scRNA_beads_readStructure.json ].'%_root_dir)
    parser.add_argument('--oligoconfig', metavar='JASON',help='whitelist file in JSON format for oligo fastq, the value of oligo barcode is an array in the JSON, [ defalut is %s/config/DNBelabC4_scRNA_oligo_readStructure.json ].'%_root_dir,)
    parser.add_argument('--oligotype', metavar='FILE',help='Whitelist of oligo, [ default is %s/config/oligo_type8.txt ].'%_root_dir)
    parser.add_argument('--expectNum', metavar='INT',type=int, help='The number of beads intercepted by the inflection point, you are not satisfied with the number of cells in the result report, then decide whether to define this parameter or not.')
    parser.add_argument('--process', metavar='TEXT',help='Custom your analysis steps, steps are separated by comma, [ default is all step, include data,count,analysis,report ].')
    parser.add_argument('--nosecondary',action='store_true',help='Disable secondary analysis, include data,count.')
    parser.add_argument('--include_introns', action='store_true',help='Include intronic reads in count.')
    parser.add_argument('--mixseq', action='store_true',help='cDNA and oligo sequence in same chip.')
    parser.add_argument('--no_bam', action='store_true',help='Do not generate a bam file in output dir.')
    return parser
    