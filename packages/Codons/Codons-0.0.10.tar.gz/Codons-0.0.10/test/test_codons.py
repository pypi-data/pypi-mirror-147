from shutil import rmtree
import codons
import re, os

fasta_path = os.path.join(os.path.dirname(__file__), 'genetic_sequence.fasta')
mers_sequence_path = os.path.join(os.path.dirname(__file__), 'MERS_sequence.txt')
cd = codons.Codons()

def test_init():
    cd = codons.Codons()
    
    # assert qualities of the content
    assert type(cd.codons_table) is codons.genes.CaseInsensitiveDict
    for TF in [cd.verbose, cd.printing, cd.verbose]:
        assert type(TF) is bool
    for dic in [cd.paths, cd.genes, cd.parameters]:
        assert type(dic) is dict
    for path in ['changed_codons', 'standard_table', 'amino_acid_synonyms']:
        assert type(cd.paths[path]) is str
    for string in [cd.parameters['residue_delimiter']]:
        assert type(string) is str
    for non in [cd.transcribed_sequence, cd.nucleotide_blast_results, cd.gene_fasta, cd.protein_fasta]:
        assert non is None
    for lis in [cd.protein_blast_results]:
        assert type(lis) is list
           
def test_transcribe():
    # DNA -> RNA
    rna_sequence = cd.transcribe(fasta_path = fasta_path)
    original_sequence = cd.sequence
    assert not re.search('[tT]', rna_sequence)
                   
    # RNA -> DNA
    dna_sequence2 = cd.transcribe(rna_sequence)
    assert original_sequence == dna_sequence2
           
def test_translate():
    # translate into a protein
    cd.translate(fasta_path = fasta_path)
    
    # assert qualities of the execution   
    assert type(cd.genes) is dict
    for string in [cd.protein_fasta,]:
        assert type(string) is str
    for lis in [cd.missed_codons, cd.parameters['start_codons']]:
        assert type(lis) is list
    for pro in [cd.genes[gene]['protein'] for gene in cd.genes]:
        assert type(pro['sequence']) is str
        assert type(pro['mass']) is str
                                     
def test_make_fasta():
    sequence, description, fasta = cd.read_fasta(fasta_path = mers_sequence_path)
    asterix = True
    if not re.search('\*', sequence[0]):
        asterix = False
    fasta = cd.make_fasta(sequence, description)
    
    # affirm the generation of the FASTA file
    descriptions = []
    sequences = []
    first = True
    seq = ''
    for line in fasta.splitlines():
        if re.search('>', line):
            line = line.replace('>', '')
            descriptions.append(line)
            if not first:
                if not asterix:
                    seq = seq.replace('*', '')
                sequences.append(seq)
            else:
                first = False
        else:
            seq += line
    if sequences == []:
        if not asterix:
            seq = seq.replace('*', '')
        sequences.append(seq)
    assert sequences == sequence
    description = [description[0]+f' - {len(sequence[0]+"*")}']
    assert descriptions == description

            
# ============== The search requires an excessive amount of time for a unit-test; nevertheless, the logic is provided ===================
#def test_blast_protein():
#    cd.translate(fasta_path = fasta_path)
#    cd.blast_protein()
#    
#    # assert qualities of the search
#    assert os.path.exists(cd.paths['protein_blast_results'])
#    rmtree(cd.paths['protein_blast_results'])
#                   
#def test_blast_nucleotide():
#    cd.blast_nucleotide(fasta_path = fasta_path)
#
#    # assert qualities of the search
#    assert os.path.exists(cd.paths['nucleotide_blast_results'])
#    rmtree(cd.paths['nucleotide_blast_results'])