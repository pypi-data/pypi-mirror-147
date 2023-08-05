# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 00:33:29 2022

@author: Andrew Freiburger
"""
from Bio.Blast import NCBIWWW #, NCBIXML
from deepdiff import DeepDiff
from pprint import pprint
from warnings import warn
from chemw import Proteins
#from pprint import pprint
from math import ceil
from glob import glob
import requests, io
import datetime
import difflib
import json, os, re

# allows case insensitive dictionary searches
class CaseInsensitiveDict(dict):   # sourced from https://stackoverflow.com/questions/2082152/case-insensitive-dictionary
    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, str) else key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
        self._convert_keys()
        
    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))
    
    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(self.__class__._k(key), value)
        
    def __delitem__(self, key):
        return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))
    
    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))
    
    def has_key(self, key):
        return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))
    
    def pop(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).pop(self.__class__._k(key), *args, **kwargs)
    
    def get(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).get(self.__class__._k(key), *args, **kwargs)
    
    def setdefault(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).setdefault(self.__class__._k(key), *args, **kwargs)
    
    def update(self, E=None, **F):
        super(CaseInsensitiveDict, self).update(self.__class__(E))
        super(CaseInsensitiveDict, self).update(self.__class__(**F))
        
    def _convert_keys(self):
        for k in list(self.keys()):
            v = super(CaseInsensitiveDict, self).pop(k)
            self.__setitem__(k, v)
            
            

class Codons():
    def __init__(self,
                 sequence: str = None,  # the genetic sequence can be optionally provided, for easy use in the other functions.
                 codons_table: str = 'standard', # the translation table for codons to amino acids
                 amino_acids_form: str = 'one_letter', # selects the scale of amino acid nomenclature
                 hyphenated: bool = None, # selects whether the printed protein will be hyphenated between the protein residues
                 verbose: bool = False,
                 printing: bool = True
                 ):
        self.verbose = verbose
        self.printing = printing
        self.genes = {}
        self.transcribed_sequence = None
        self.protein_blast_results = []
        self.nucleotide_blast_results = None
        self.gene_fasta = None
        self.protein_fasta = None
        self.protein_mass = Proteins(printing = False)
        
        # define the simulation paths
        self.paths = {}
        self.paths['changed_codons'] = os.path.join(os.path.dirname(__file__), 'rosetta_stone', 'changed_codons.json')
        self.paths['standard_table'] = os.path.join(os.path.dirname(__file__), 'rosetta_stone', 'standard_table.json')
        self.paths['amino_acid_synonyms'] = os.path.join(os.path.dirname(__file__), 'rosetta_stone', 'amino_acid_synonyms.json')
        
        self.parameters = {}
        self.parameters['residue_delimiter'] = '-' 
        
        # refine the sequence into the FASTA format
        self.sequence = sequence
        
        # define the proper codons table
        with open(self.paths['standard_table']) as codons:
            self.codons_table = json.load(codons)
        if codons_table != 'standard':
            self._convert_codon_tables(codons_table)    
        self.codons_table = CaseInsensitiveDict(self.codons_table)
        
        # define the amino acid nomenclature
        if amino_acids_form != 'full_name':
            with open(self.paths['amino_acid_synonyms']) as aas:
                self.amino_acid_synonyms = json.load(aas)
            for codon in self.codons_table:
                amino_acid = self.codons_table[codon] 
                if amino_acid not in ['stop', 'start']:
                    self.codons_table[codon] = self.amino_acid_synonyms[amino_acid][amino_acids_form]
            
            if amino_acids_form == 'one_letter' and not hyphenated:
                self.parameters['residue_delimiter'] = ''
                
    
    def _convert_codon_tables(self,codons_table):
        # convert the standard table into the desired table
        with open(self.paths['changed_codons']) as new_codons:
            self.changed_codons = json.load(new_codons)
        if codons_table not in self.changed_codons:
            raise IndexError(f'The {codons_table} parameter is not presently supported by the options: {list(self.changed_codons.keys())}. Edit the < changed_codons.json > file to offer the exchanges that you desire for your simulation.')
            
        self.changed_codons = self.changed_codons[codons_table]
        for cd in self.changed_codons:
            self.codons_table[cd] = self.changed_codons[cd]
    
    def read_fasta(self,
                    fasta_path: str = None,  # the path to the fasta file
                    fasta_link: str = None,  # the url to the fasta file
                    ):
        # import and parse fasta-formatted files        
        if fasta_path is not None:
            with open(fasta_path) as input:
                self.fasta_lines = input.readlines()   
        elif fasta_link is not None:
            sequence = requests.get(fasta_link).content
            self.fasta_lines = io.StringIO(sequence.decode('utf-8')).readlines()
    
        sequences = []
        descriptions = []
        seq = ''
        first = True
        for line in self.fasta_lines:
            if not re.search('(^>)', line):
                seq += line.rstrip()
            else:
                if first:
                    first = False
                    continue
                descriptions.append(str(line))
                sequences.append(str(seq))
                seq = ''
        if sequences == []:
            sequences.append(seq)
            seq = re.sub('([^A-Z])', '', seq, flags = re.IGNORECASE)
            descriptions.append(' - '.join(['Sequence', f'{len(seq)}_monomers']))
                
        return sequences, descriptions, self.make_fasta(sequences, descriptions)
    
    def _paths(self, 
               export_name = None, 
               export_directory = None
               ):
        # define the simulation_path
        if export_directory is None:
            export_directory = os.getcwd()
        elif not os.path.exists(export_directory):
            os.mkdir(export_directory)

        tag = ''
        if self.genes != {}:
            tag = f'{len(self.genes)}_proteins'
        elif self.transcribed_sequence:
            tag = f'{self.transcription}'
        if export_name is None:
            export_name = '-'.join([re.sub(' ', '_', str(x)) for x in ['codons', tag]])
            
        count = -1
        export_path = os.path.join(export_directory, export_name)
        file_extension = ''
        while os.path.exists(export_path):
            count += 1
            if re.search(r'(\.[a-zA-Z]+$)', export_path):
                file_extension = re.search(r'(\.[a-zA-Z]+$)', export_path).group()
                export_path = re.sub(file_extension, '', export_path)
                
            if not re.search('(-[0-9]+$)', export_path):
                export_path += f'-{count}'   
            else:
                export_path = re.sub('([0-9]+)$', str(count), export_path)
                
            export_path += file_extension
        
        # clean the export name
        export_path = re.sub('(--)', '-', export_path)
        export_path = re.sub('(-$)', '', export_path)
            
        return export_path
            
    def make_fasta(self,
                   sequences: str,  # the genetic nucleotide sequence
                   descriptions: str = 'sequence', # the description of the genetic or protein sequence
                   export_path: str = None
                   ):
        if sequences is None:
            return None
            
        if type(sequences) is list:
            fasta_file = []
            for index, sequence in enumerate(sequences):
                description = descriptions
                if type(descriptions) is list:
                    description = descriptions[index]
                if not '*' in sequence:
                    sequence += '*'
                fasta = '\n'.join(['>'+' - '.join([description, f'{len(sequence)}']), sequence])
                fasta_file.append(fasta)
            fasta_file = '\n'.join(fasta_file)
        elif type(sequences) is str:
            if not '*' in sequences:
                sequences += '*'
            fasta_file = '\n'.join(['>'+descriptions, sequences])
        else:
            ValueError(f'The sequence type {type(sequences)} is not supported by the function.')
        
        if export_path is not None:
            with open(export_path, 'w') as out:
                out.write(fasta_file)
        
        return fasta_file
    
    def complement(self,
                   sequence: str = None, # the genetic sequence for which the complemenentary strand will be determined
                   dna: bool = True      # specifies whether the parameterized strand is DNA or RNA
                   ):
        complementary_strand = ''
        for nuc in sequence:
            if nuc == 'a':
                if dna:
                    complementary_strand += 't'
                else:
                    complementary_strand += 'u'
            elif nuc == 'A':
                if dna:
                    complementary_strand += 'T'
                else:
                    complementary_strand += 'U'
            if nuc == 't':
                complementary_strand += 'a'
            elif nuc == 'T':
                complementary_strand += 'A'
            if nuc == 'u':
                complementary_strand += 'a'
            elif nuc == 'U':
                complementary_strand += 'A'
            if nuc == 'c':
                complementary_strand += 'g'
            elif nuc == 'C':
                complementary_strand += 'G'
            if nuc == 'g':
                complementary_strand += 'c'
            elif nuc == 'G':
                complementary_strand += 'c'
                
        return complementary_strand
            
    def transcribe(self,
                   sequence: str = None,    # the genomic code as a string
                   description: str = '',   # a description of the sequence
                   fasta_path: str = None,  # the path to the fasta file
                   fasta_link: str = None,  # the path to the fasta file
                   ):
        if sequence:
            self.sequence = sequence
            base_pairs = len(re.sub("([^atcgu])", "", self.sequence, flags = re.IGNORECASE))
            unit = 'bp'
            if base_pairs > 1e4:
                unit = 'kbp'
            self.gene_fasta = self.make_fasta(self.sequence, ' - '.join(['Genetic_sequence', f'{base_pairs}_{unit}']))
        elif fasta_path:
            sequences, descriptions, self.gene_fasta = self.read_fasta(fasta_path)
            self.sequence = sequences[0]
        elif fasta_link:
            sequences, descriptions, self.gene_fasta = self.read_fasta(fasta_link = fasta_link)
            self.sequence = sequences[0]
            
        # determine the capitalization of the sequence
        for ch in self.sequence:
            if re.search('[a-zA-Z]',ch): 
                upper_case = ch.isupper()
                break
            
        # substitute the nucleotides with the appropriate capitalization
        self.transcription = 'DNA_to_RNA'
        if re.search('u|U', self.sequence):
            self.transcription = 'RNA_to_DNA'
            if upper_case:
                self.transcribed_sequence = re.sub('U', 'T', self.sequence)
            else:
                self.transcribed_sequence = re.sub('u', 't', self.sequence)
        if re.search('t|T', self.sequence):
            if upper_case:
                self.transcribed_sequence = re.sub('T', 'U', self.sequence)
            else:
                self.transcribed_sequence = re.sub('t', 'u', self.sequence)
                
        print('The sequence is transcribed.')
        if not description:
            description = f'>Transcribed sequence from {self.transcription}'
        self.transcribed_fasta = self.make_fasta(self.transcribed_sequence, description)
        return self.transcribed_sequence
    
    def find_start(self,i, sequence):
        starts = '(?=' + '|'.join(self.parameters['start_codons']) + ')'            
        codon = ''
        while not re.search(starts, codon, flags=re.IGNORECASE) and i < len(self.sequence):
            codon = self.sequence[i:i+3]
            i += 1
        if re.search('[a-z]{3}', codon, flags=re.IGNORECASE):
            self.amino_acids = [self.codons_table[codon]]
        i += 2
        return i
        
    def translate(self,
                 sequence: str = None, # the genomic code as a string
                 fasta_path: str = None,  # the path to the fasta file
                 fasta_link: str = None,  # the path to the fasta file
                 organism: str = 'bacteria', # specifies the organism whose genome is being translated
                 start_codons: list = None, # the list of start codons that are accepted by the code
                 all_possible_proteins: bool = False, # generates all possible proteins from a given genetic sequence
                 open_reading_frames: bool = True,  # translate each of the three possible open reading frames for a specified sequence
                 filter_protein_size: int = 30, # the smallest peptide size that will still be included in the set of translated proteins
                 sense_strand_translation: bool = False # specifies whether the sense strand, complementary to the parameterzied sequence, will be translated as well
                 ):
        def end_protein(start_i,end_i, loop, gene, codons):
            protein = self.parameters['residue_delimiter'].join(self.amino_acids)
            mass = self.protein_mass.mass(protein)
            
            strand = '+' if loop <= 3 else '-'
            if loop > 3:
                loop -= 3
            description = ' - '.join(['Protein', f'{len(self.amino_acids)}_residues', f'{mass}_amu', f'{start_i}-{end_i} bp', f'({strand}{loop}) ORF'])
            fasta_file = self.make_fasta(protein, description)
            self.genes[gene] = {}
            self.genes[gene]['protein'] = {
                    'sequence': protein,
                    'mass': mass
            }
            self.genes[gene]['codons'] = codons
            self.protein_fasta.append(fasta_file)
            
        def chemical_translation(i, start_i, loop):
            codons = []                
            codon = ''
            gene = ''
            for nuc in sequence[start_i:]:
                i += 1
                gene += nuc
                codon += nuc
                if len(codon) == 3:
                    codons.append(codon)
                    if codon not in self.codons_table:
                        self.missed_codons.append(codon)
                    else:
                        amino_acid = self.codons_table[codon]
                        if amino_acid == 'stop':
                            if len(self.amino_acids) >= filter_protein_size:
                                end_protein(start_i, i, loop, gene, codons)
                            break
                        else:
                            self.amino_acids.append(amino_acid)
                            if self.verbose:
                                print(codon, '\t', amino_acid)
                    codon = ''
                elif i+2 >= len(sequence):
                    if len(self.amino_acids) >= filter_protein_size:
                        end_protein(start_i, i, loop, gene, codons)
                    self.amino_acids = None
                    break
            return i
        
        # establish the conditions
        self.parameters['start_codons'] = start_codons
        if start_codons == None:
            if organism == 'bacteria':
                self.parameters['start_codons'] = ['ATG', 'AUG', 'GTG', "GUG"]
            elif organism == 'virus':
                self.parameters['start_codons'] = ['ATG', 'AUG']
            else:
                warn('ERROR: The organism type must be either bacteria or virus')
                
        if sequence:
            self.sequence = sequence
            self.gene_fasta = self.make_fasta(self.sequence, ' - '.join(['Genetic_sequence', f'{len(self.sequence)}_bps']))
        elif fasta_path:
            sequences, descriptions, self.gene_fasta = self.read_fasta(fasta_path)
            self.sequence = sequences[0]
        elif fasta_link:
            sequences, descriptiosn, self.gene_fasta = self.read_fasta(fasta_link = fasta_link)
            print(sequences)
            self.sequence = sequences[0]

        self.sequence = re.sub('([^atucg])', '', self.sequence, flags = re.IGNORECASE)
        sequences = [self.sequence]
        if open_reading_frames:
            sequences = [self.sequence, self.sequence[1:], self.sequence[2:]]  
        if sense_strand_translation:
            self.complementary_sequence = self.complement(self.sequence)
            sequences.append(self.complementary_sequence)
            if open_reading_frames:
                sequences.extend([self.complementary_sequence[1:], self.complementary_sequence[2:]])
        
        # translate the sequence
        self.protein_fasta, self.missed_codons = [], []
        loop = 0
        for sequence in sequences: 
            if not all_possible_proteins:
                loop += 1
            i = 0
            while i < len(sequence):
                i = start_i = self.find_start(i, sequence)
                if i > len(sequence)-10:
                    break
                i = chemical_translation(i, start_i, loop)
                if all_possible_proteins:
                    i = start_i
                    
        if self.verbose:
            if loop == 3:
                sequence_proteins = dict(self.genes)
                print('sequence_proteins', len(sequence_proteins))
            elif loop > 3:
                complement_proteins = DeepDiff(sequence_proteins, self.genes,ignore_order=True, report_repetition=True)
                print(complement_proteins.pretty())
#                    with open("complement_proteins.json", "w") as out_file:
#                        json.dump(dict(complement_proteins), out_file, indent = 4)
                print('complement_proteins', len(self.genes)-len(sequence_proteins))
                
        self.protein_fasta = '\n'.join(self.protein_fasta)
        if self.printing:       
            print(self.protein_fasta)
            if self.missed_codons != []:
                print(f'The {self.missed_codons} codons were not captured by the employed codons table.')
            
    
    def blast_protein(self,  # https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome
                      sequence: str = None,
                      database: str = 'nr', # the blastp database that will be searched with the collected FASTA sequences
                      description: str = 'Protein sequence description',  
                      fasta_path: str = None, # The path to a fasta file
                      fasta_link: str = None,  # the path to the fasta file
                      export_name = 'codons-BLASTp', 
                      export_directory = None
                      ):
        if sequence:
            self.sequence = sequence 
            sequences = [sequence]
            self.protein_fasta = self.make_fasta(sequence, description) 
        elif fasta_path:
            sequences, descriptions, self.protein_fasta = self.read_fasta(fasta_path = fasta_path)
        elif fasta_link:
            sequences, descriptions, self.protein_fasta = self.read_fasta(fasta_link = fasta_link)
            
        # estimate the completion time
        estimated_time = datetime.datetime.now()+datetime.timedelta(seconds = len(self.protein_fasta)*1.4)
        print(f'The database search for the parameterized protein(s) will complete circa {estimated_time}.')
        
        # acquire the BLAST results
        self.export(export_name, export_directory)
        self.paths['protein_blast_results'] = [os.path.join(self.export_path, 'protein_blast_results.xml')]
        for index, sequence in enumerate(sequences):
            short_query = False
            if len(sequence) < 30:
                short_query = True
            if len(sequence) > 1000:
                sequence = sequence[:1000]
            protein_result = NCBIWWW.qblast('blastp', database, sequence, short_query = short_query)
            self.protein_blast_results.append(protein_result)
            result = protein_result.read()
                        
            # export this modular portion
            export_path = self._paths('protein_blast_results.xml', self.export_path)
            self.paths['protein_blast_results'].append(export_path)
            with open(self.paths['protein_blast_results'][-1], 'w') as protein_data:
                protein_data.write(result)
                    
            print(f' \rCompleted searches: {index+1}/{len(sequences)}\t{datetime.datetime.now()}', end='')
                    
        return self.protein_blast_results
        
    def blast_nucleotide(self,
                         sequence: str = None,
                         database: str = 'nt',
                         description: str = 'Genetic sequence description',  # a description of the sequence
                         fasta_path: str = None, # The path to a fasta file
                         fasta_link: str = None,  # the path to the fasta file
                         export_name = 'codons-BLASTn', 
                         export_directory = None
                         ):
        self.nucleotide_blast_results = []
        if sequence:
            self.sequence = sequence 
            sequences = [sequence]
            self.gene_fasta = self.make_fasta(sequence, description) 
        elif fasta_path:
            sequences, descriptions, self.gene_fasta = self.read_fasta(fasta_path = fasta_path)
        elif fasta_link:
            sequences, descriptions, self.gene_fasta = self.read_fasta(fasta_link = fasta_link)
                        
        # estimate the completion time
        estimated_length = len(self.gene_fasta)/2
        estimated_time = datetime.datetime.now()+datetime.timedelta(seconds = estimated_length/2)    # approximately 1/2 second per nucleic acid
        print(f'The database search for the parameterized genetic sequence will complete circa {estimated_time}.')
        
        # acquire the BLAST results
        self.export(export_name, export_directory)
        self.paths['nucleotide_blast_results'] = []
        
        section_size = 4000
        for sequence in sequences:
            sections = ceil(len(sequence)/section_size)
            sequence_sections = [sequence[i*section_size:(i+1)*section_size] for i in range(0, sections)]
            for index, seq in enumerate(sequence_sections):
                nucleotide_blast_result = NCBIWWW.qblast('blastn', database, seq)
                self.nucleotide_blast_results.append(nucleotide_blast_result)
                result = nucleotide_blast_result.read()
                
                # export this modular portion
                export_path = self._paths(f'blastn_section{index}_results.xml', self.export_path)
                self.paths['nucleotide_blast_results'].append(export_path)
                with open(self.paths['nucleotide_blast_results'][-1], 'w',encoding='utf8') as nucleotide_data:
                    nucleotide_data.write(result)
                
                print(f'Section {index+1}/{len(sequence_sections)} is completed:\t{datetime.datetime.now()}')
                        
        return self.nucleotide_blast_results
                
    def export(self, export_name = None, export_directory = None):
        # define the simulation_path
        self.export_path = self._paths(export_name, export_directory)
        if not os.path.exists(self.export_path):
            os.mkdir(self.export_path)
        
        # export the genetic and protein sequences
        if self.gene_fasta:
            self.paths['genetic_sequence'] = os.path.join(self.export_path, 'genetic_sequence.fasta')
            with open(self.paths['genetic_sequence'], 'w',encoding='utf8') as genes:
                genes.write(self.gene_fasta)
            
        if self.genes != {}:
            self.paths['protein_sequence'] = os.path.join(self.export_path, 'protein_sequence.fasta')
            with open(self.paths['protein_sequence'], 'w') as proteins:
                proteins.write(self.protein_fasta)
            
        if self.transcribed_sequence:
            self.paths['transcribed_sequence'] = os.path.join(self.export_path, 'transcribed_sequence.fasta')
            with open(self.paths['transcribed_sequence'], 'w') as genes:
                genes.write(self.transcribed_fasta)                 