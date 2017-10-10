import datetime
import os
import urllib
from django import forms
from django.core.files.storage import FileSystemStorage
from django.http import Http404
from progress.models import JobStatus
from sRNAtoolboxweb.settings import BASE_DIR
from FileModels.speciesParser import SpeciesParser
from sRNAtoolboxweb.settings import MEDIA_ROOT
from utils.pipeline_utils import generate_uniq_id
from django.conf import settings
from django.core.files.base import ContentFile

SPECIES_PATH = settings.CONF["species"]

from FileModels.TargetConsensusParser import TargetConsensusParser

complete_species = {}
species_file = SpeciesParser(SPECIES_PATH)
array_species = species_file.parse()





class MirconsForm(forms.Form):


    #for sp in array_species:
     #   complete_species[sp[4]]=None


    mirfile = forms.FileField(label='Upload miRNAs file', required=False)
    utrfile = forms.FileField(label='Upload targets file', required=False)

    mirtext = forms.CharField(label="Or paste your miRNAs here",widget=forms.Textarea,required=False)
    utrtext = forms.CharField(label="Or paste your targets here",widget=forms.Textarea,required=False)

    plants = forms.BooleanField(label='Is plant analysis', required=False)

    targetspy=forms.BooleanField(label='TargetSpy', required=False)
    miranda=forms.BooleanField(label='Miranda', required=False)
    PITA=forms.BooleanField(label='PITA', required=False)
    psRobot=forms.BooleanField(label='psRobot', required=False)
    tapir_fasta=forms.BooleanField(label='TAPIR FASTA engine', required=False)
    tapir_RNAhyb=forms.BooleanField(label='TAPIR RNAhybrid engine', required=False)

    target_par=forms.CharField(label="TargetSpy parameters",required=False)
    miranda_par = forms.CharField(label="Miranda Parameters", required=False)
    PITA_par = forms.CharField(label="PITA parameters", required=False)
    psRobot_par=forms.CharField(label="psRobot parameters",required=False)
    tapir_fa_par = forms.CharField(label="TAPIR FASTA parameters", required=False)
    tapir_RNA_par = forms.CharField(label="TAPIR RNA parameters", required=False)


    def clean(self):
        cleaned_data = super(MirconsForm, self).clean()
        if not cleaned_data.get('mirfile') and not cleaned_data.get('mirtext'):
            self.add_error('mirfile', 'miRNA input is required')
            self.add_error('mirtext', 'miRNA input is required')
        if not cleaned_data.get('utrfile') and not cleaned_data.get('utrtext'):
            self.add_error('utrfile', 'UTR input is required')
            self.add_error('utrtext', 'UTR input is required')
        if not cleaned_data.get('targetspy') and not cleaned_data.get('miranda') and not cleaned_data.get('PITA') and not cleaned_data.get('psRobot') and not cleaned_data.get('tapir_fasta') and not cleaned_data.get('tapir_RNAhyb'):
            self.add_error('targetspy', 'At least one program should be chosen')
            self.add_error('miranda', 'At least one program should be chosen')
            self.add_error('PITA', 'At least one program should be chosen')
            self.add_error('psRobot', 'At least one program should be chosen')
            self.add_error('tapir_fasta', 'At least one program should be chosen')
            self.add_error('tapir_RNAhyb', 'At least one program should be chosen')
        return cleaned_data

    def generate_id(self):
        is_new = True
        while is_new:
            pipeline_id = generate_uniq_id()
            if not JobStatus.objects.filter(pipeline_key=pipeline_id):
                return pipeline_id

    def create_call(self):

        pipeline_id = self.generate_id()
        FS = FileSystemStorage()
        FS.location = os.path.join(MEDIA_ROOT, pipeline_id)
        os.system("mkdir " + FS.location)
        out_dir = FS.location
        mirfile = self.cleaned_data.get("mirfile")
        utrfile= self.cleaned_data.get("utrfile")
        program_list=[]
        if self.cleaned_data.get('targetspy'):
            program_list.append("targetspy")
        if self.cleaned_data.get('miranda'):
            program_list.append("miranda")
        if self.cleaned_data.get('PITA'):
            program_list.append("PITA")
        if self.cleaned_data.get('psRobot'):
            program_list.append("psRobot")
        if self.cleaned_data.get('tapir_fasta'):
            program_list.append("tapir_fasta")
        if self.cleaned_data.get('tapir_RNAhyb'):
            program_list.append("tapir_RNAhyb")
        program_string = ":".join(program_list)
        if mirfile:
            file_to_update = mirfile
            uploaded_file = str(file_to_update)
            mirfile = FS.save(uploaded_file, file_to_update)
        else:
            mirtext=self.cleaned_data.get("mirtext")
            content = ContentFile(mirtext)
            mirfile=FS.fileUpload.save("mirs.fa", content)
            FS.save()
        if utrfile:
            file_to_update = utrfile
            uploaded_file = str(file_to_update)
            utrfile = FS.save(uploaded_file, file_to_update)
        else:
            utrtext = self.cleaned_data.get("utrtext")
            content = ContentFile(utrtext)
            utrfile=FS.fileUpload.save('utrs.fa', content)
            FS.save()

        name = pipeline_id + '_mirconstarget'
        JobStatus.objects.create(job_name=name, pipeline_key=pipeline_id, job_status="not launched",
                                 start_time=datetime.datetime.now(),
                                 #finish_time=datetime.time(0, 0),
                                 all_files=ifile,
                                 modules_files="",
                                 pipeline_type="mirconstarget",
                                )
        return 'qsub -v pipeline="mirconstarget",program_string="{program_string}",parameter_string="{}",'.format(
            pipeline_id=pipeline_id,
            out_dir=out_dir,
            miRNA_file=mirfile,
            utr_file=utrfile,
            program_string=program_string,
            input_file=os.path.join(FS.location, ifile),
            string=self.cleaned_data.get("string"),
            name=name,
            job_name=name,
            sh=os.path.join(BASE_DIR + '/core/bash_scripts/run_mirnatarget.sh')
        )

###########ADDING
        #'",parameter_string="' + parameter_string + '",key="' + pipeline_id + '",outdir="' + outdir + '",miRNA_file="' + miRNA_file + '",utr_file="' + utr_file +
        #'",name="' + pipeline_id + '_mirconstarget"' + ' -N ' + pipeline_id + '_mirconstarget

        #return 'qsub -v pipeline="mirconstarget",program_string="{program_string}",key="{pipeline_id}",outdir="{out_dir}",inputfile="{input_file}",string="{string}",remove="true",name="{name}" -N {job_name} {sh}'.format(