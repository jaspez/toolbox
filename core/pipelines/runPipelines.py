__author__ = 'antonior'
import sys
from pipelines import *
import argparse


def functerms(args):
    parameters = "\n".join(["Input: "+args.input.split("/")[-1], "Annotations: "+args.annotations, "Species: "+args.specie, "Experimental Targets Only: " + args.exp])
    new_pipe = sRNAfuncTermsPipeline(args.annotations.split(","), args.pipelineKey, args.jobName, args.outdir,
                                     args.input, args.specie, args.type, args.exp, parameters)

    new_pipe.run()


def bench(args):
    parameters = "".join([line for line in file(args.configure).readlines() if "desc" not in line and "libs" not in line and not "maintaingOrig" in line and not "zip" in line and not "graphics" in line]).replace("=", ": ").replace("/shared/", "").replace("sRNAtoolbox/webData/", "")
    new_pipe = sRNAbenchPipeline(args.pipelineKey, args.jobName, args.outdir, args.configure, parameters)
    new_pipe.run()



def de(args):
    parameters = "\n".join(["Input: "+args.input.split("/")[-1], "Groups: "+str(args.groups), "Sample Description: " + str(args.sampleDesc),
                            "Threshold Noiseq: "+str(args.noiseq_threshold), "Thresholds deSeq/EdgeR: "+str(args.deseq_threshold),
                            "IsoMir Analysis: "+ str(args.iso)])


    new_pipe = sRNAdePipeline(args.pipelineKey, args.jobName, args.outdir, args.input, args.groups, args.sampleDesc,
                              args.noiseq_threshold, args.deseq_threshold, args.iso, args.hm_Perc, args.hm_top,
                              args.matrixDesc, parameters)
    new_pipe.run()



def blast(args):
    parameters = "".join([line for line in file(args.configure).readlines() if "output" not in line and "minRC" not in line and not "blastn" in line ]).replace("=", ": ").replace("/shared/", "").replace("sRNAtoolbox/webData/", "")
    new_pipe = sRNAblastPipeline(args.pipelineKey, args.jobName, args.outdir, args.configure, parameters)
    new_pipe.run()



def jbrowser(args):
    parameters = "\n".join(["sRNAbenchId: " + args.bench_id])
    new_pipe = sRNAjBrowserPipeline(args.pipelineKey, args.jobName, args.outdir, args.bench_id, parameters)
    new_pipe.run()


def mirconstarget(args):

    parameter_string = args.parameter_string.replace("55-55", "-")
    parameters = "\n".join(["miRNAs File: "+args.mirna_file.split("/")[-1], "UTRs File: "+args.utr_file.split("/")[-1],
                            "Programs: "+args.program_string, "Programs Parameters: "+ parameter_string])
    new_pipe = mirconstargetPipeline(args.pipelineKey, args.jobName, args.outdir, args.mirna_file, args.utr_file,
                                   args.threads, args.program_string, parameter_string, parameters)
    new_pipe.run()


def gfree(args):
    parameters = ""
    new_pipe = sRNAgFreePipeline(args.pipelineKey, args.jobName, args.outdir, args.input, args.minReadLength,
                     args.maxReadLength, args.microRNA, args.minRC, args.novelStrict, args.noMM, parameters)

    new_pipe.run()


def helper(args):
    dic_arg={}
    if args.mode:
        dic_arg["mode"]=args.mode
    if args.inputfile:
        dic_arg["inputfile"]=args.inputfile
    if args.species:
        dic_arg["species"]=args.species
    if args.taxon:
        dic_arg["taxon"]=args.taxon
    if args.string:
        dic_arg["string"]=args.string
    if args.remove:
        dic_arg["remove"]=args.remove

    parameters = "\n".join([key+": "+ dic_arg[key] for key in dic_arg])
    new_pipe = helpersPipelines(args.pipelineKey, args.jobName, args.outdir, parameters, **dic_arg)
    new_pipe.run()


def mirnafunctargets(args):
    parameter_string = args.parameter_string.replace("55-55", "-")
    parameters = "\n".join(["miRNAs File: "+args.mirna_file.split("/")[-1], "UTRs File: "+args.utr_file.split("/")[-1],
                            "Programs: "+args.program_string, "Programs Parameters: "+parameter_string, "Species: "+args.species])

    new_pipe = mirconsfunctargetPipeline(args.pipelineKey, args.jobName, args.outdir, args.mirna_file, args.utr_file,
                                         args.threads, args.program_string, parameter_string, args.species, parameters)
    new_pipe.run()


def dejbrowser(args):
    if args.length is not None:
        parameters = "\n".join(["sRNAbenchId: " + args.bench_id, "Sample Groups:"+args.groups, "Length Intervals: "+args.length])
    else:
        parameters = "\n".join(["sRNAbenchId: " + args.bench_id, "Sample Groups:"+args.groups])
    new_pipe = sRNAdejBrowserPipeline(args.pipelineKey, args.jobName, args.outdir, args.bench_id, args.groups, args.length, parameters)
    new_pipe.run()


def main():
    parser = argparse.ArgumentParser(description='Launch all sRNAtoolbox Pipelines')
    parser.add_argument('pipelineKey', help='Identifier to pipeline')
    parser.add_argument('jobName', help='Name of the Job')
    parser.add_argument('outdir', help='outdir')
    subparsers = parser.add_subparsers(help='Pipeline Name', description="Pipeline Name", dest="tool")

    functerm_parser = subparsers.add_parser('functerms', help='Launch SRNAfuncterms')
    de_parser = subparsers.add_parser('de', help='Launch de')
    dejbrowser_parser = subparsers.add_parser('dejbrowser', help='Launch dejbrowser')
    bench_parser = subparsers.add_parser('bench', help='Launch bench')
    blast_parser = subparsers.add_parser('blast', help='Launch blast')
    jbrowser_parser = subparsers.add_parser('jbrowser', help='Launch jbrowser')
    mirconstarget_parser = subparsers.add_parser('mirconstarget', help='Launch mirconstarget')
    gfree_parser = subparsers.add_parser('gfree', help='Launch gfree')
    helper_parser = subparsers.add_parser('helper', help='Launch helper')
    mirnafunctarget_parser = subparsers.add_parser('mirnafunctargets', help='Launch mirnafunctargets')

    functerm_parser.add_argument('-a', dest='annotations', required=True,
                                 help='Requiered. Comma separated annontations')
    functerm_parser.add_argument('-i', dest='input', required=True,
                                 help='Required. path to miRNA input file. Default=None')
    functerm_parser.add_argument('-t', dest='type', default='list', help='Optional. pipeline type. Default=list')
    functerm_parser.add_argument('--specie', dest='specie', required=True, help='Optional. Species')
    functerm_parser.add_argument('--exp', dest='exp', required=True, help='Optional. Species')

    bench_parser.add_argument('-c', dest='configure', required=True, help='Requiered. Configuration file')
    blast_parser.add_argument('-c', dest='configure', required=True, help='Requiered. Configuration file')

    de_parser.add_argument('-g', dest='groups', default=None, help='Optional. Configuration file')
    de_parser.add_argument('-i', dest='input', required=True, help='Requiered. Input (string of ids or matrix file)')
    de_parser.add_argument('--iso', dest='iso', required=True, help='Optional. Run isoMir Analysis')
    de_parser.add_argument('-d', dest='sampleDesc', default=None, help='Optional. Description')
    de_parser.add_argument('--desc', dest='matrixDesc', default=None, help='Optional. Description')
    de_parser.add_argument('--nt', dest='noiseq_threshold', help='Optional. Noiseq threshold')
    de_parser.add_argument('--dt', dest='deseq_threshold', help='Optional. Deseq threshold')
    de_parser.add_argument('--hmTop', dest='hm_top', help='Optional. hhmTop threshold')
    de_parser.add_argument('--hmPerc', dest='hm_Perc', help='Optional. hmPerc threshold')

    jbrowser_parser.add_argument('--bench_id', dest='bench_id', required=True, help='Requiered. sRNABench id')

    dejbrowser_parser.add_argument('--bench_id', dest='bench_id', required=True, help='Requiered. sRNABench id')
    dejbrowser_parser.add_argument('--groups', dest='groups', required=True, help='Requiered. groups')
    dejbrowser_parser.add_argument('--length', dest='length', help='Optional. length')

    mirconstarget_parser.add_argument('--mirna_file', dest='mirna_file', required=True, help='Requiered. mirnas file')
    mirconstarget_parser.add_argument('--utr_file', dest='utr_file', required=True, help='Requiered. utrs file')
    mirconstarget_parser.add_argument('-p', dest='threads', default="4", help='Optional. number of threads')
    mirconstarget_parser.add_argument('--program_string', dest='program_string', required=True,
                                    help='Requiered. program string')
    mirconstarget_parser.add_argument('--parameter_string', dest='parameter_string', default="",
                                    help='Optional. parameter string')

    gfree_parser.add_argument('-i', dest='input', required=True, help='Requiered. Input')
    gfree_parser.add_argument('--minReadLength', dest='minReadLength', required=True, help='Requiered. minReadLength')
    gfree_parser.add_argument('--maxReadLength', dest='maxReadLength', required=True, help='Requiered. maxReadLength')
    gfree_parser.add_argument('--microRNA', dest='microRNA', required=True, help='Requiered. microRNA')
    gfree_parser.add_argument('--minRC', dest='minRC', required=True, help='Requiered. minRC')
    gfree_parser.add_argument('--novelStrict', dest='novelStrict', default="true", help='Optional. novelStrict')
    gfree_parser.add_argument('--noMM', dest='noMM', required=True, help='Requiered. noMM')

    helper_parser.add_argument('--mode', dest='mode', required=True, help='Requiered. mode')
    helper_parser.add_argument('--inputfile', dest='inputfile', required=False, help='Requiered. inputfile')
    helper_parser.add_argument('--species', dest='species', required=False, help='Optional. species')
    helper_parser.add_argument('--taxon', dest='taxon', required=False, help='Optional. taxon')
    helper_parser.add_argument('--string', dest='string', required=False, help='Optional. string')
    helper_parser.add_argument('--remove', dest='remove', required=False, help='Optional. remove')

    mirnafunctarget_parser.add_argument('--mirna_file', dest='mirna_file', required=True, help='Requiered. mirnas file')
    mirnafunctarget_parser.add_argument('--utr_file', dest='utr_file', required=True, help='Requiered. utrs file')
    mirnafunctarget_parser.add_argument('-p', dest='threads', default="4", help='Optional. number of threads')
    mirnafunctarget_parser.add_argument('--program_string', dest='program_string', required=True,
                                        help='Requiered. program string')
    mirnafunctarget_parser.add_argument('--parameter_string', dest='parameter_string', default="",
                                        help='Optional. parameter string')
    mirnafunctarget_parser.add_argument('--species', dest='species', required=True, help='Optional. Species')


    args = parser.parse_args()

    if args.tool == "functerms":
        functerms(args)

    if args.tool == "bench":
        bench(args)

    if args.tool == "de":
        de(args)

    if args.tool == "blast":
        blast(args)

    if args.tool == "jbrowser":
        jbrowser(args)

    if args.tool == "mirconstarget":
        mirconstarget(args)

    if args.tool == "gfree":
        gfree(args)

    if args.tool == "mirnafunctargets":
        mirnafunctargets(args)

    if args.tool == "dejbrowser":
        dejbrowser(args)


    if args.tool == "helper":
        print "helper"
        helper(args)


if __name__ == '__main__':
    main()
















