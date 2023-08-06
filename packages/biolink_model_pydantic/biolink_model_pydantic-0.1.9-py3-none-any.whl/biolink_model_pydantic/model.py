# Auto generated from biolink-model.yaml by pydanticgen.py version: 0.9.0
# Generation date: 2022-04-19T10:04:56
# Schema: Biolink-Model
#
# id: https://w3id.org/biolink/biolink-model
# description: Entity and association taxonomy and datamodel for life-sciences data
# license: https://creativecommons.org/publicdomain/zero/1.0/

from __future__ import annotations

import datetime
import logging
import re
from collections import namedtuple
from dataclasses import field
from enum import Enum, unique
from typing import Any, ClassVar, List, Optional, Union

from pydantic import constr, validator
from pydantic.dataclasses import dataclass

LOG = logging.getLogger(__name__)

metamodel_version = "1.7.0"
curie_regexp = (
    r'^[a-zA-Z_]?[a-zA-Z_0-9.-]*:([A-Za-z0-9_][A-Za-z0-9_.-]*[A-Za-z0-9./\(\)\-><_:;]*)?$'
)
curie_pattern = re.compile(curie_regexp)

# Type Aliases
Unit = Union[int, float]
LabelType = str
IriType = constr(regex=r'^(http|ftp)')
Curie = constr(regex=curie_regexp)
URIorCURIE = Union[Curie, IriType]
CategoryType = URIorCURIE
NarrativeText = str
XSDDate = datetime.date
TimeType = datetime.time
SymbolType = str
FrequencyValue = str
PercentageFrequencyValue = float
BiologicalSequence = str
Quotient = float
Bool = bool

# Namespaces

valid_prefix = {
    "AAO",
    "ABS",
    "ACEVIEW_WORM",
    "ACLAME",
    "ADW",
    "AEO",
    "AERO",
    "AFFY_PROBESET",
    "AFTOL_TAXONOMY",
    "AGD",
    "AGRICOLA",
    "AGRO",
    "ALLERGOME",
    "AMOEBADB",
    "ANTIBODYREGISTRY",
    "ANTWEB",
    "AOP",
    "AOP_EVENTS",
    "AOP_RELATIONSHIPS",
    "AOP_STRESSOR",
    "APB",
    "APD",
    "APHIDBASE_TRANSCRIPT",
    "APID_INTERACTIONS",
    "APO",
    "AQTLPub",
    "AQTLTrait",
    "ARACHNOSERVER",
    "ARDB",
    "ARK",
    "ARO",
    "ARRAYEXPRESS",
    "ARRAYEXPRESS_PLATFORM",
    "ARRAYMAP",
    "ARXIV",
    "ASAP",
    "ASCL",
    "ASIN",
    "ASPGD_LOCUS",
    "ASPGD_PROTEIN",
    "ATC",
    "ATCC",
    "ATCVET",
    "ATFDB_FAMILY",
    "ATO",
    "AUTDB",
    "AspGD",
    "BACMAP_BIOG",
    "BACMAP_MAP",
    "BAO",
    "BCGO",
    "BCO",
    "BDGP_EST",
    "BDGP_INSERTION",
    "BEETLEBASE",
    "BEGDB",
    "BFO",
    "BGEE_FAMILY",
    "BGEE_GENE",
    "BGEE_ORGAN",
    "BGEE_STAGE",
    "BIGG_COMPARTMENT",
    "BIGG_METABOLITE",
    "BIGG_MODEL",
    "BIGG_REACTION",
    "BILA",
    "BIND",
    "BINDINGDB",
    "BIOCARTA_PATHWAY",
    "BIOCATALOGUE_SERVICE",
    "BIOCYC",
    "BIOGRID",
    "BIOMINDER",
    "BIOMODELS_DB",
    "BIOMODELS_KISAO",
    "BIOMODELS_TEDDY",
    "BIOMODELS_VOCABULARY",
    "BIONUMBERS",
    "BIOPORTAL",
    "BIOPROJECT",
    "BIOSAMPLE",
    "BIOSYSTEMS",
    "BIOTOOLS",
    "BITTERDB_CPD",
    "BITTERDB_REC",
    "BNODE",
    "BOLD_TAXONOMY",
    "BOOTSTREP",
    "BRENDA",
    "BROAD",
    "BSPO",
    "BT",
    "BTO",
    "BUGBASE_EXPT",
    "BUGBASE_PROTOCOL",
    "BYKDB",
    "CABRI",
    "CAID",
    "CAMEO",
    "CAPS",
    "CARO",
    "CAS",
    "CATH",
    "CATH_DOMAIN",
    "CATH_SUPERFAMILY",
    "CATTLEQTLDB",
    "CAZY",
    "CCDS",
    "CCO",
    "CDAO",
    "CDD",
    "CDPD",
    "CELLIMAGE",
    "CELLOSAURUS",
    "CEPH",
    "CGD",
    "CGSC",
    "CHADO",
    "CHARPROT",
    "CHEBI",
    "CHEMBL_COMPOUND",
    "CHEMBL_MECHANISM",
    "CHEMBL_TARGET",
    "CHEMDB",
    "CHEMIDPLUS",
    "CHEMINF",
    "CHEMSPIDER",
    "CHICKENQTLDB",
    "CHMO",
    "CHR",
    "CID",
    "CIO",
    "CL",
    "CLDB",
    "CLINICALTRIALS",
    "CLINVAR",
    "CLINVAR_RECORD",
    "CLINVAR_SUBMISSION",
    "CLO",
    "CLUSTR",
    "CMF",
    "CMMR",
    "CMO",
    "CMR_GENE",
    "COAR_RESOURCE",
    "COG",
    "COGS",
    "COGS_FUNCTION",
    "COMBINE_SPECIFICATIONS",
    "COMPLEXPORTAL",
    "COMPTOX",
    "COMPULYEAST",
    "CONOSERVER",
    "CORIELL",
    "CORUM",
    "COSMIC",
    "CPC",
    "CPT",
    "CRISPRDB",
    "CRO",
    "CRYPTODB",
    "CSA",
    "CST",
    "CST_AB",
    "CTD",
    "CTD_CHEMICAL",
    "CTD_DISEASE",
    "CTD_GENE",
    "CTENO",
    "CUBEDB",
    "CVDO",
    "CYGD",
    "ChemBank",
    "ClinVarSubmitters",
    "ClinVarVariant",
    "CoriellCollection",
    "CoriellFamily",
    "CoriellIndividual",
    "D1ID",
    "DAILYMED",
    "DARC",
    "DASHR",
    "DASHR_EXPRESSION",
    "DATA",
    "DATF",
    "DBD",
    "DBEST",
    "DBG2INTRONS",
    "DBGAP",
    "DBPROBE",
    "DBSNP",
    "DC_CL",
    "DDANAT",
    "DDPHENO",
    "DECIPHER",
    "DEGRADOME",
    "DEPOD",
    "DEV_GA4GHDOS",
    "DGIdb",
    "DICTYBASE_EST",
    "DICTYBASE_GENE",
    "DIDEO",
    "DINTO",
    "DIP",
    "DISPROT",
    "DOID",
    "DOID-PROPERTY",
    "DOMMINO",
    "DOOR",
    "DOQCS_MODEL",
    "DOQCS_PATHWAY",
    "DPV",
    "DRAGONDB_ALLELE",
    "DRAGONDB_DNA",
    "DRAGONDB_LOCUS",
    "DRAGONDB_PROTEIN",
    "DRON",
    "DRSC",
    "DRUGBANK",
    "DRUGBANKV4_TARGET",
    "DRUGBANK_TARGET",
    "DUO",
    "DrugCentral",
    "EBIMETAGENOMICS_PROJ",
    "EBIMETAGENOMICS_SAMP",
    "EC",
    "EC-CODE",
    "ECHOBASE",
    "ECO",
    "ECOCORE",
    "ECOGENE",
    "ECOLIWIKI",
    "ECTO",
    "ECYANO_ENTITY",
    "ECYANO_MODEL",
    "ECYANO_RULE",
    "EDAM",
    "EDAM-DATA",
    "EDAM-FORMAT",
    "EDAM-OPERATION",
    "EDAM-TOPIC",
    "EFO",
    "EGA_DATASET",
    "EGA_STUDY",
    "EGGNOG",
    "EHDA",
    "EHDAA",
    "EHDAA2",
    "ELM",
    "EMAP",
    "EMAPA",
    "EMDB",
    "EMMA",
    "ENA_EMBL",
    "ENCODE",
    "ENSEMBL",
    "ENSEMBL_BACTERIA",
    "ENSEMBL_FUNGI",
    "ENSEMBL_METAZOA",
    "ENSEMBL_PLANT",
    "ENSEMBL_PROTIST",
    "ENVO",
    "EO",
    "EOM",
    "EPD",
    "EPO",
    "ERO",
    "ERV",
    "EU89H",
    "EUCLINICALTRIALS",
    "EUPATH",
    "EV",
    "EXAC_GENE",
    "EXAC_TRANSCRIPT",
    "EXAC_VARIANT",
    "ExO",
    "FACEBASE",
    "FAIRSHARING",
    "FAO",
    "FB",
    "FBOL",
    "FBSP",
    "FBbi",
    "FBbt",
    "FBcv",
    "FBdv",
    "FDADrug",
    "FIX",
    "FLOPO",
    "FLU",
    "FLYSTOCK",
    "FMA",
    "FOODON",
    "FPLX",
    "FSNP",
    "FUNCAT",
    "FUNCBASE_FLY",
    "FUNCBASE_HUMAN",
    "FUNCBASE_MOUSE",
    "FUNCBASE_YEAST",
    "FUNGIDB",
    "FYECO",
    "FYPO",
    "FlyBase",
    "GA4GHDOS",
    "GABI",
    "GAMMA",
    "GAZ",
    "GDC",
    "GENATLAS",
    "GENECARDS",
    "GENEDB",
    "GENEFARM",
    "GENEPIO",
    "GENETREE",
    "GENEWIKI",
    "GENO",
    "GENPEPT",
    "GENPROP",
    "GEO",
    "GIARDIADB",
    "GINAS",
    "GLIDA_GPCR",
    "GLIDA_LIGAND",
    "GLYCOEPITOPE",
    "GLYCOMEDB",
    "GLYTOUCAN",
    "GMD",
    "GMD_ANALYTE",
    "GMD_GCMS",
    "GMD_PROFILE",
    "GMD_REF",
    "GNPIS",
    "GO",
    "GOA",
    "GOLD_GENOME",
    "GOLD_META",
    "GOOGLE_PATENT",
    "GOP",
    "GOREL",
    "GO_REF",
    "GPCRDB",
    "GPMDB",
    "GRAMENE_GENE",
    "GRAMENE_GROWTHSTAGE",
    "GRAMENE_PROTEIN",
    "GRAMENE_QTL",
    "GRAMENE_TAXONOMY",
    "GREENGENES",
    "GRID",
    "GRIN_TAXONOMY",
    "GRO",
    "GRSDB",
    "GSID",
    "GTEx",
    "GTOPDB",
    "GUDMAP",
    "GWASCENTRAL_MARKER",
    "GWASCENTRAL_PHENOTYPE",
    "GWASCENTRAL_STUDY",
    "GXA_EXPT",
    "GXA_GENE",
    "GenBank",
    "GeneReviews",
    "HABRONATTUS",
    "HAMAP",
    "HANCESTRO",
    "HAO",
    "HCPCS",
    "HCVDB",
    "HDR",
    "HGMD",
    "HGNC",
    "HGNC_FAMILY",
    "HGNC_GENEFAMILY",
    "HGNC_SYMBOL",
    "HINV_LOCUS",
    "HINV_PROTEIN",
    "HINV_TRANSCRIPT",
    "HMDB",
    "HOGENOM",
    "HOM",
    "HOMD_SEQ",
    "HOMD_TAXON",
    "HOMOLOGENE",
    "HOVERGEN",
    "HP",
    "HPA",
    "HPM_PEPTIDE",
    "HPM_PROTEIN",
    "HPO",
    "HPRD",
    "HSSP",
    "HUGE",
    "HsapDv",
    "IAO",
    "ICD",
    "ICD10",
    "ICD9",
    "ICEBERG_ELEMENT",
    "ICEBERG_FAMILY",
    "ICO",
    "IDEAL",
    "IDO",
    "IDOMAL",
    "IEV",
    "IMEX",
    "IMGT_HLA",
    "IMGT_LIGM",
    "IMG_GENE",
    "IMG_TAXON",
    "IMPC",
    "IMPRESS-parameter",
    "IMPRESS-procedure",
    "IMPRESS-protocol",
    "IMR",
    "INCHI",
    "INCHIKEY",
    "INO",
    "INSDC",
    "INSDC_CDS",
    "INSDC_GCA",
    "INSDC_SRA",
    "INTACT",
    "INTACT_MOLECULE",
    "IPI",
    "IPR",
    "IRD_SEGMENT",
    "IREFWEB",
    "ISBN-10",
    "ISBN-13",
    "ISFINDER",
    "IUPHAR_FAMILY",
    "IUPHAR_LIGAND",
    "IUPHAR_RECEPTOR",
    "J",
    "JAX",
    "JAXMICE",
    "JCGGDB",
    "JCM",
    "JCSD",
    "JSTOR",
    "JWS",
    "KEGG",
    "KEGG-ds",
    "KEGG-hsa",
    "KEGG-ko",
    "KEGG-path",
    "KEGG_BRITE",
    "KEGG_COMPOUND",
    "KEGG_DGROUP",
    "KEGG_DISEASE",
    "KEGG_DRUG",
    "KEGG_ENVIRON",
    "KEGG_ENZYME",
    "KEGG_GENE",
    "KEGG_GENES",
    "KEGG_GENOME",
    "KEGG_GLYCAN",
    "KEGG_METAGENOME",
    "KEGG_MODULE",
    "KEGG_ORTHOLOGY",
    "KEGG_PATHWAY",
    "KEGG_RCLASS",
    "KEGG_REACTION",
    "KISAO",
    "KNAPSACK",
    "LGIC",
    "LICEBASE",
    "LIGANDBOX",
    "LIGANDEXPO",
    "LINCS_CELL",
    "LINCS_DATA",
    "LINCS_PROTEIN",
    "LINCS_SMALLMOLECULE",
    "LIPIDBANK",
    "LIPIDMAPS",
    "LIPRO",
    "LOGGERHEAD",
    "LOINC",
    "LPT",
    "LRG",
    "MA",
    "MACIE",
    "MAIZEGDB_LOCUS",
    "MAMO",
    "MAO",
    "MASSBANK",
    "MASSIVE",
    "MAT",
    "MATRIXDB_ASSOCIATION",
    "MAXO",
    "MDM",
    "MEDDRA",
    "MEDLINEPLUS",
    "MEROPS",
    "MEROPS_FAMILY",
    "MEROPS_INHIBITOR",
    "MESH",
    "MESH_2012",
    "MESH_2013",
    "METABOLIGHTS",
    "METACYC_COMPOUND",
    "METANETX_CHEMICAL",
    "METANETX_COMPARTMENT",
    "METANETX_REACTION",
    "METLIN",
    "MEX",
    "MF",
    "MFMO",
    "MFO",
    "MFOEM",
    "MFOMD",
    "MGI",
    "MI",
    "MIAPA",
    "MICRO",
    "MICROSCOPE",
    "MICROSPORIDIA",
    "MIM",
    "MIMODB",
    "MINID",
    "MINT",
    "MIPMOD",
    "MIR",
    "MIRBASE_MATURE",
    "MIREX",
    "MIRIAM_COLLECTION",
    "MIRIAM_RESOURCE",
    "MIRNAO",
    "MIRNEST",
    "MIRO",
    "MIRTARBASE",
    "MMDB",
    "MMO",
    "MMP_CAT",
    "MMP_DB",
    "MMP_REF",
    "MMRRC",
    "MMUSDV",
    "MO",
    "MOBIDB",
    "MOD",
    "MODELDB",
    "MOLBASE",
    "MONARCH",
    "MONDO",
    "MOP",
    "MP",
    "MPATH",
    "MPD",
    "MPD-assay",
    "MPD-strain",
    "MPID",
    "MPIO",
    "MRO",
    "MS",
    "MSigDB",
    "MUGEN",
    "MULTICELLDS_CELL_LINE",
    "MULTICELLDS_COLLECTION",
    "MULTICELLDS_SNAPSHOT",
    "MW_PROJECT",
    "MW_STUDY",
    "MYCOBANK",
    "MYCO_LEPRA",
    "MYCO_MARINUM",
    "MYCO_SMEG",
    "MYCO_TUBER",
    "MZSPEC",
    "MmusDv",
    "MonarchArchive",
    "MonarchData",
    "NAPDI",
    "NAPP",
    "NARCIS",
    "NASC",
    "NBN",
    "NBO",
    "NBO-PROPERTY",
    "NBRC",
    "NCBIAssembly",
    "NCBIGI",
    "NCBIGene",
    "NCBIGenome",
    "NCBIPROTEIN",
    "NCBITaxon",
    "NCIM",
    "NCIMR",
    "NCIT",
    "NCIT-OBO",
    "NCRO",
    "NDC",
    "NDDF",
    "NEUROLEX",
    "NEUROMORPHO",
    "NEURONDB",
    "NEUROVAULT_COLLECTION",
    "NEUROVAULT_IMAGE",
    "NEXTDB",
    "NEXTPROT",
    "NGL",
    "NIAEST",
    "NIF_CELL",
    "NIF_DYSFUNCTION",
    "NIF_GROSSANATOMY",
    "NLMID",
    "NMR",
    "NONCODEV3",
    "NONCODEV4_GENE",
    "NONCODEV4_RNA",
    "NORINE",
    "NUCLEARBD",
    "OAE",
    "OARCS",
    "OBA",
    "OBAN",
    "OBCS",
    "OBI",
    "OBIB",
    "OBO",
    "OBOREL",
    "OBO_REL",
    "OCI",
    "OCLC",
    "ODOR",
    "OGG",
    "OGI",
    "OGMS",
    "OGSF",
    "OHD",
    "OHMI",
    "OIO",
    "OLATDV",
    "OMA_GRP",
    "OMA_PROTEIN",
    "OMIA",
    "OMIA-breed",
    "OMIABIS",
    "OMIM",
    "OMIM_PS",
    "OMIT",
    "OMP",
    "OMRSE",
    "ONTONEO",
    "OOSTT",
    "OPB",
    "OPL",
    "OPM",
    "ORCID",
    "ORDB",
    "ORIDB_SACCH",
    "ORIDB_SCHIZO",
    "ORPHA",
    "ORPHANET",
    "ORPHANET_ORDO",
    "ORTHODB",
    "ORYZABASE_GENE",
    "ORYZABASE_MUTANT",
    "ORYZABASE_STAGE",
    "ORYZABASE_STRAIN",
    "OTL",
    "OVAE",
    "P3DB_PROTEIN",
    "P3DB_SITE",
    "PAINT_REF",
    "PALEODB",
    "PANTHER",
    "PANTHER_FAMILY",
    "PANTHER_NODE",
    "PANTHER_PATHWAY",
    "PANTHER_PTHCMP",
    "PAO",
    "PASS2",
    "PATHEMA",
    "PATHWAYCOMMONS",
    "PATO",
    "PAXDB_ORGANISM",
    "PAXDB_PROTEIN",
    "PAZAR",
    "PCO",
    "PDB",
    "PDB-CCD",
    "PDB_LIGAND",
    "PDRO",
    "PDUMDV",
    "PD_ST",
    "PECO",
    "PEPTIDEATLAS",
    "PEROXIBASE",
    "PFAM",
    "PGDSO",
    "PGN",
    "PGX",
    "PHARMGKB_DISEASE",
    "PHARMGKB_DRUG",
    "PHARMGKB_GENE",
    "PHARMGKB_PATHWAYS",
    "PHAROS",
    "PHENOLEXPLORER",
    "PHOSPHOPOINT_KINASE",
    "PHOSPHOPOINT_PROTEIN",
    "PHOSPHOSITE_PROTEIN",
    "PHOSPHOSITE_RESIDUE",
    "PHYLOMEDB",
    "PHYTOZOME_LOCUS",
    "PID_PATHWAY",
    "PIGQTLDB",
    "PINA",
    "PIROPLASMA",
    "PIRSF",
    "PLANA",
    "PLANTTFDB",
    "PLASMODB",
    "PLO",
    "PMAP_CUTDB",
    "PMAP_SUBSTRATEDB",
    "PMC",
    "PMCID",
    "PMDB",
    "PMID",
    "PMP",
    "PO",
    "POCKETOME",
    "POLBASE",
    "PORO",
    "PPO",
    "PR",
    "PRIDE",
    "PRIDE_PROJECT",
    "PRINTS",
    "PROBONTO",
    "PRODOM",
    "PROGLYC",
    "PROPREO",
    "PROSITE",
    "PROTCLUSTDB",
    "PROTEOMICSDB_PEPTIDE",
    "PROTEOMICSDB_PROTEIN",
    "PROTONET_CLUSTER",
    "PROTONET_PROTEINCARD",
    "PSCDB",
    "PSEUDOMONAS",
    "PSIMI",
    "PSIPAR",
    "PUBCHEM_BIOASSAY",
    "PUBCHEM_COMPOUND",
    "PUBCHEM_SUBSTANCE",
    "PUBMED",
    "PW",
    "PX",
    "PathWhiz",
    "PomBase",
    "RBK",
    "RBRC",
    "REACT",
    "REACTOME",
    "REBASE",
    "REFSEQ",
    "REPODB",
    "RESID",
    "REX",
    "RFAM",
    "RGD",
    "RGDRef",
    "RGD_QTL",
    "RGD_STRAIN",
    "RHEA",
    "RICEGAP",
    "RICENETDB_COMPOUND",
    "RICENETDB_GENE",
    "RICENETDB_MIRNA",
    "RICENETDB_PROTEIN",
    "RICENETDB_REACTION",
    "RNACENTRAL",
    "RNAMODS",
    "RNAO",
    "RO",
    "ROUGE",
    "RRID",
    "RS",
    "RXCUI",
    "RXNO",
    "RXNORM",
    "ResearchID",
    "SABIORK_EC",
    "SABIORK_KINETICRECORD",
    "SABIORK_REACTION",
    "SAO",
    "SASBDB",
    "SBO",
    "SCIENCESIGNALING_PATH",
    "SCIENCESIGNALING_PDC",
    "SCIENCESIGNALING_PIC",
    "SCOP",
    "SCRETF",
    "SDBS",
    "SEED",
    "SEED_COMPOUND",
    "SEED_REACTION",
    "SEMMEDDB",
    "SEP",
    "SEPIO",
    "SGD",
    "SGD_PATHWAYS",
    "SGD_REF",
    "SGN",
    "SHEEPQTLDB",
    "SIBO",
    "SIDER_DRUG",
    "SIDER_EFFECT",
    "SIGNALING-GATEWAY",
    "SIO",
    "SISU",
    "SITEX",
    "SMART",
    "SMPDB",
    "SNOMED",
    "SNOMEDCT",
    "SO",
    "SOPHARM",
    "SOYBASE",
    "SPD",
    "SPIKE_MAP",
    "SPLASH",
    "STAP",
    "STATO",
    "STITCH",
    "STOREDB",
    "STRING",
    "STY",
    "SUBTILIST",
    "SUBTIWIKI",
    "SUGARBIND",
    "SUPFAM",
    "SWH",
    "SWISS-MODEL",
    "SWISSLIPID",
    "SWISSREGULON",
    "SWO",
    "SYMP",
    "ScopusID",
    "SwissProt",
    "T3DB",
    "TADS",
    "TAHE",
    "TAHH",
    "TAIR",
    "TAIR_GENE",
    "TAIR_LOCUS",
    "TAIR_PROTEIN",
    "TAO",
    "TARBASE",
    "TAXONOMY",
    "TAXRANK",
    "TCDB",
    "TGD",
    "TGMA",
    "TIGRFAM",
    "TISSUELIST",
    "TO",
    "TOL",
    "TOPDB",
    "TOPFIND",
    "TOXOPLASMA",
    "TRANS",
    "TREEBASE",
    "TREEFAM",
    "TRICHDB",
    "TRITRYPDB",
    "TTD_DRUG",
    "TTD_TARGET",
    "TTO",
    "TrEMBL",
    "UBERGRAPH",
    "UBERON",
    "UBERON_CORE",
    "UBERON_NONAMESPACE",
    "UBIO_NAMEBANK",
    "UCSC",
    "UMBBD_COMPOUND",
    "UMBBD_ENZYME",
    "UMBBD_PATHWAY",
    "UMBBD_REACTION",
    "UMBBD_RULE",
    "UMLS",
    "UMLSSG",
    "UNIGENE",
    "UNII",
    "UNIMOD",
    "UNIPARC",
    "UNIPATHWAY",
    "UNIPATHWAY_COMPOUND",
    "UNIPATHWAY_REACTION",
    "UNIPROT",
    "UNIPROT_ISOFORM",
    "UNISTS",
    "UNITE",
    "UO",
    "UO-PROPERTY",
    "UPHENO",
    "USPTO",
    "UniProtKB",
    "VALIDATORDB",
    "VANDF",
    "VARIO",
    "VBASE2",
    "VBRC",
    "VECTORBASE",
    "VFDB_GENE",
    "VFDB_GENUS",
    "VHOG",
    "VIPR",
    "VIRALZONE",
    "VIRSIRNA",
    "VIVO",
    "VMC",
    "VMHMETABOLITE",
    "VMHREACTION",
    "VO",
    "VSAO",
    "VT",
    "VTO",
    "WB",
    "WBBT",
    "WBLS",
    "WBPhenotype",
    "WBVocab",
    "WB_RNAI",
    "WBbt",
    "WBls",
    "WD_Entity",
    "WD_Prop",
    "WIKIDATA",
    "WIKIDATA_PROPERTY",
    "WIKIGENES",
    "WIKIPATHWAYS",
    "WIKIPEDIA_EN",
    "WORFDB",
    "WORMPEP",
    "WORMS",
    "WormBase",
    "XAO",
    "XCO",
    "XL",
    "XPO",
    "Xenbase",
    "YDPM",
    "YEASTINTRON",
    "YETFASCO",
    "YID",
    "YPO",
    "YRCPDR",
    "ZEA",
    "ZECO",
    "ZFA",
    "ZFIN",
    "ZFIN_EXPRESSION",
    "ZFIN_PHENOTYPE",
    "ZFS",
    "ZINC",
    "ZP",
    "alliancegenome",
    "apollo",
    "biolink",
    "bioschemas",
    "catfishQTL",
    "cattleQTL",
    "chickenQTL",
    "dbSNPIndividual",
    "dbVar",
    "dc",
    "dcat",
    "dcid",
    "dct",
    "dcterms",
    "dctypes",
    "dictyBase",
    "doi",
    "fabio",
    "faldo",
    "foaf",
    "foodb_compound",
    "gff3",
    "gpi",
    "gtpo",
    "horseQTL",
    "idot",
    "interpro",
    "isbn",
    "isni",
    "issn",
    "linkml",
    "medgen",
    "metacyc_reaction",
    "mirbase",
    "mmmp_biomaps",
    "oa",
    "oboInOwl",
    "oboformat",
    "os",
    "owl",
    "pav",
    "pigQTL",
    "prov",
    "qud",
    "rainbow_troutQTL",
    "rdf",
    "rdfs",
    "schema",
    "sheepQTL",
    "shex",
    "skos",
    "uuid",
    "void",
    "wgs",
    "xml",
    "xsd",
}


# Pydantic Config
class PydanticConfig:
    """
    Pydantic config
    https://pydantic-docs.helpmanual.io/usage/model_config/
    """

    validate_assignment = True
    validate_all = True
    underscore_attrs_are_private = True
    extra = 'forbid'
    arbitrary_types_allowed = True  # TODO re-evaluate this


# Pydantic Validators
def check_curie_prefix(cls, curie: Union[List, str, None]):
    if isinstance(curie, list):
        for cur in curie:
            prefix = cur.split(':')[0]
            if prefix not in valid_prefix:

                LOG.warning(f"{curie} prefix '{prefix}' not in curie map")
                if hasattr(cls, '_id_prefixes') and cls._id_prefixes:
                    LOG.warning(f"Consider one of {cls._id_prefixes}")
                else:
                    LOG.warning(
                        f"See https://biolink.github.io/biolink-model/context.jsonld "
                        f"for a list of valid curie prefixes"
                    )
    elif curie:
        prefix, local_id = curie.split(':', 1)
        if prefix not in valid_prefix:
            LOG.warning(f"{curie} prefix '{prefix}' not in curie map")
            if hasattr(cls, '_id_prefixes') and cls._id_prefixes:
                LOG.warning(f"Consider one of {cls._id_prefixes}")
            else:
                LOG.warning(
                    f"See https://biolink.github.io/biolink-model/context.jsonld "
                    f"for a list of valid curie prefixes"
                )
        if local_id == '':
            LOG.warning(f"{curie} does not have a local identifier")


def convert_scalar_to_list_check_curies(cls, value: Any) -> List[str]:
    """
    Converts list fields that have been passed a scalar to a 1-sized list

    Also checks prefix checks curies.  Because curie regex constraints
    are applied prior to running this function, we can use this for both
    curie and non-curie fields by rechecking re.match(curie_pattern, some_string)
    """
    if not isinstance(value, list):
        value = [value]
    for val in value:
        if isinstance(val, str) and re.match(curie_pattern, val):
            check_curie_prefix(cls, val)
    return value


def check_value_is_not_none(slotname: str, value: Any):
    is_none = False
    if isinstance(value, list) or isinstance(value, dict):
        if not field:
            is_none = True
    else:
        if value is None:
            is_none = True

    if is_none:
        raise ValueError(f"{slotname} is required")


# Predicates
@unique
class PredicateType(str, Enum):
    """
    Enum for biolink predicates
    """

    abundance_affected_by = "biolink:abundance_affected_by"
    abundance_decreased_by = "biolink:abundance_decreased_by"
    abundance_increased_by = "biolink:abundance_increased_by"
    active_in = "biolink:active_in"
    actively_involved_in = "biolink:actively_involved_in"
    actively_involves = "biolink:actively_involves"
    activity_affected_by = "biolink:activity_affected_by"
    activity_decreased_by = "biolink:activity_decreased_by"
    activity_increased_by = "biolink:activity_increased_by"
    acts_upstream_of = "biolink:acts_upstream_of"
    acts_upstream_of_negative_effect = "biolink:acts_upstream_of_negative_effect"
    acts_upstream_of_or_within = "biolink:acts_upstream_of_or_within"
    acts_upstream_of_or_within_negative_effect = (
        "biolink:acts_upstream_of_or_within_negative_effect"
    )
    acts_upstream_of_or_within_positive_effect = (
        "biolink:acts_upstream_of_or_within_positive_effect"
    )
    acts_upstream_of_positive_effect = "biolink:acts_upstream_of_positive_effect"
    adverse_event_caused_by = "biolink:adverse_event_caused_by"
    affected_by = "biolink:affected_by"
    affects = "biolink:affects"
    affects_abundance_of = "biolink:affects_abundance_of"
    affects_activity_of = "biolink:affects_activity_of"
    affects_degradation_of = "biolink:affects_degradation_of"
    affects_expression_in = "biolink:affects_expression_in"
    affects_expression_of = "biolink:affects_expression_of"
    affects_folding_of = "biolink:affects_folding_of"
    affects_localization_of = "biolink:affects_localization_of"
    affects_metabolic_processing_of = "biolink:affects_metabolic_processing_of"
    affects_molecular_modification_of = "biolink:affects_molecular_modification_of"
    affects_mutation_rate_of = "biolink:affects_mutation_rate_of"
    affects_response_to = "biolink:affects_response_to"
    affects_risk_for = "biolink:affects_risk_for"
    affects_secretion_of = "biolink:affects_secretion_of"
    affects_splicing_of = "biolink:affects_splicing_of"
    affects_stability_of = "biolink:affects_stability_of"
    affects_synthesis_of = "biolink:affects_synthesis_of"
    affects_transport_of = "biolink:affects_transport_of"
    affects_uptake_of = "biolink:affects_uptake_of"
    ameliorates = "biolink:ameliorates"
    approved_for_treatment_by = "biolink:approved_for_treatment_by"
    approved_to_treat = "biolink:approved_to_treat"
    associated_with = "biolink:associated_with"
    associated_with_resistance_to = "biolink:associated_with_resistance_to"
    associated_with_sensitivity_to = "biolink:associated_with_sensitivity_to"
    author = "biolink:author"
    biomarker_for = "biolink:biomarker_for"
    broad_match = "biolink:broad_match"
    capability_of = "biolink:capability_of"
    capable_of = "biolink:capable_of"
    catalyzes = "biolink:catalyzes"
    caused_by = "biolink:caused_by"
    causes = "biolink:causes"
    causes_adverse_event = "biolink:causes_adverse_event"
    chemically_interacts_with = "biolink:chemically_interacts_with"
    chemically_similar_to = "biolink:chemically_similar_to"
    close_match = "biolink:close_match"
    coexists_with = "biolink:coexists_with"
    coexpressed_with = "biolink:coexpressed_with"
    colocalizes_with = "biolink:colocalizes_with"
    completed_by = "biolink:completed_by"
    composed_primarily_of = "biolink:composed_primarily_of"
    condition_associated_with_gene = "biolink:condition_associated_with_gene"
    consumed_by = "biolink:consumed_by"
    consumes = "biolink:consumes"
    contains_process = "biolink:contains_process"
    contraindicated_for = "biolink:contraindicated_for"
    contributes_to = "biolink:contributes_to"
    contribution_from = "biolink:contribution_from"
    contributor = "biolink:contributor"
    correlated_with = "biolink:correlated_with"
    decreased_amount_in = "biolink:decreased_amount_in"
    decreases_abundance_of = "biolink:decreases_abundance_of"
    decreases_activity_of = "biolink:decreases_activity_of"
    decreases_amount_or_activity_of = "biolink:decreases_amount_or_activity_of"
    decreases_degradation_of = "biolink:decreases_degradation_of"
    decreases_expression_of = "biolink:decreases_expression_of"
    decreases_folding_of = "biolink:decreases_folding_of"
    decreases_localization_of = "biolink:decreases_localization_of"
    decreases_metabolic_processing_of = "biolink:decreases_metabolic_processing_of"
    decreases_molecular_interaction = "biolink:decreases_molecular_interaction"
    decreases_molecular_modification_of = "biolink:decreases_molecular_modification_of"
    decreases_mutation_rate_of = "biolink:decreases_mutation_rate_of"
    decreases_response_to = "biolink:decreases_response_to"
    decreases_secretion_of = "biolink:decreases_secretion_of"
    decreases_splicing_of = "biolink:decreases_splicing_of"
    decreases_stability_of = "biolink:decreases_stability_of"
    decreases_synthesis_of = "biolink:decreases_synthesis_of"
    decreases_transport_of = "biolink:decreases_transport_of"
    decreases_uptake_of = "biolink:decreases_uptake_of"
    degradation_affected_by = "biolink:degradation_affected_by"
    degradation_decreased_by = "biolink:degradation_decreased_by"
    degradation_increased_by = "biolink:degradation_increased_by"
    derives_from = "biolink:derives_from"
    derives_into = "biolink:derives_into"
    develops_from = "biolink:develops_from"
    develops_into = "biolink:develops_into"
    diagnoses = "biolink:diagnoses"
    directly_interacts_with = "biolink:directly_interacts_with"
    disease_has_basis_in = "biolink:disease_has_basis_in"
    disease_has_location = "biolink:disease_has_location"
    disrupted_by = "biolink:disrupted_by"
    disrupts = "biolink:disrupts"
    editor = "biolink:editor"
    enabled_by = "biolink:enabled_by"
    enables = "biolink:enables"
    entity_negatively_regulated_by_entity = "biolink:entity_negatively_regulated_by_entity"
    entity_negatively_regulates_entity = "biolink:entity_negatively_regulates_entity"
    entity_positively_regulated_by_entity = "biolink:entity_positively_regulated_by_entity"
    entity_positively_regulates_entity = "biolink:entity_positively_regulates_entity"
    entity_regulated_by_entity = "biolink:entity_regulated_by_entity"
    entity_regulates_entity = "biolink:entity_regulates_entity"
    exacerbates = "biolink:exacerbates"
    exact_match = "biolink:exact_match"
    expressed_in = "biolink:expressed_in"
    expresses = "biolink:expresses"
    expression_affected_by = "biolink:expression_affected_by"
    expression_decreased_by = "biolink:expression_decreased_by"
    expression_increased_by = "biolink:expression_increased_by"
    folding_affected_by = "biolink:folding_affected_by"
    folding_decreased_by = "biolink:folding_decreased_by"
    folding_increased_by = "biolink:folding_increased_by"
    food_component_of = "biolink:food_component_of"
    gene_associated_with_condition = "biolink:gene_associated_with_condition"
    gene_product_of = "biolink:gene_product_of"
    genetic_association = "biolink:genetic_association"
    genetically_interacts_with = "biolink:genetically_interacts_with"
    has_active_ingredient = "biolink:has_active_ingredient"
    has_biomarker = "biolink:has_biomarker"
    has_catalyst = "biolink:has_catalyst"
    has_completed = "biolink:has_completed"
    has_contraindication = "biolink:has_contraindication"
    has_decreased_amount = "biolink:has_decreased_amount"
    has_excipient = "biolink:has_excipient"
    has_food_component = "biolink:has_food_component"
    has_frameshift_variant = "biolink:has_frameshift_variant"
    has_gene_product = "biolink:has_gene_product"
    has_increased_amount = "biolink:has_increased_amount"
    has_input = "biolink:has_input"
    has_manifestation = "biolink:has_manifestation"
    has_metabolite = "biolink:has_metabolite"
    has_missense_variant = "biolink:has_missense_variant"
    has_molecular_consequence = "biolink:has_molecular_consequence"
    has_nearby_variant = "biolink:has_nearby_variant"
    has_negative_upstream_actor = "biolink:has_negative_upstream_actor"
    has_negative_upstream_or_within_actor = "biolink:has_negative_upstream_or_within_actor"
    has_non_coding_variant = "biolink:has_non_coding_variant"
    has_nonsense_variant = "biolink:has_nonsense_variant"
    has_not_completed = "biolink:has_not_completed"
    has_nutrient = "biolink:has_nutrient"
    has_output = "biolink:has_output"
    has_part = "biolink:has_part"
    has_participant = "biolink:has_participant"
    has_phenotype = "biolink:has_phenotype"
    has_plasma_membrane_part = "biolink:has_plasma_membrane_part"
    has_positive_upstream_actor = "biolink:has_positive_upstream_actor"
    has_positive_upstream_or_within_actor = "biolink:has_positive_upstream_or_within_actor"
    has_real_world_evidence_of_association_with = (
        "biolink:has_real_world_evidence_of_association_with"
    )
    has_sequence_location = "biolink:has_sequence_location"
    has_sequence_variant = "biolink:has_sequence_variant"
    has_splice_site_variant = "biolink:has_splice_site_variant"
    has_substrate = "biolink:has_substrate"
    has_synonymous_variant = "biolink:has_synonymous_variant"
    has_target = "biolink:has_target"
    has_upstream_actor = "biolink:has_upstream_actor"
    has_upstream_or_within_actor = "biolink:has_upstream_or_within_actor"
    has_variant_part = "biolink:has_variant_part"
    homologous_to = "biolink:homologous_to"
    in_cell_population_with = "biolink:in_cell_population_with"
    in_complex_with = "biolink:in_complex_with"
    in_linkage_disequilibrium_with = "biolink:in_linkage_disequilibrium_with"
    in_pathway_with = "biolink:in_pathway_with"
    in_taxon = "biolink:in_taxon"
    increased_amount_of = "biolink:increased_amount_of"
    increases_abundance_of = "biolink:increases_abundance_of"
    increases_activity_of = "biolink:increases_activity_of"
    increases_amount_or_activity_of = "biolink:increases_amount_or_activity_of"
    increases_degradation_of = "biolink:increases_degradation_of"
    increases_expression_of = "biolink:increases_expression_of"
    increases_folding_of = "biolink:increases_folding_of"
    increases_localization_of = "biolink:increases_localization_of"
    increases_metabolic_processing_of = "biolink:increases_metabolic_processing_of"
    increases_molecular_interaction = "biolink:increases_molecular_interaction"
    increases_molecular_modification_of = "biolink:increases_molecular_modification_of"
    increases_mutation_rate_of = "biolink:increases_mutation_rate_of"
    increases_response_to = "biolink:increases_response_to"
    increases_secretion_of = "biolink:increases_secretion_of"
    increases_splicing_of = "biolink:increases_splicing_of"
    increases_stability_of = "biolink:increases_stability_of"
    increases_synthesis_of = "biolink:increases_synthesis_of"
    increases_transport_of = "biolink:increases_transport_of"
    increases_uptake_of = "biolink:increases_uptake_of"
    interacts_with = "biolink:interacts_with"
    is_active_ingredient_of = "biolink:is_active_ingredient_of"
    is_diagnosed_by = "biolink:is_diagnosed_by"
    is_excipient_of = "biolink:is_excipient_of"
    is_frameshift_variant_of = "biolink:is_frameshift_variant_of"
    is_input_of = "biolink:is_input_of"
    is_metabolite_of = "biolink:is_metabolite_of"
    is_missense_variant_of = "biolink:is_missense_variant_of"
    is_molecular_consequence_of = "biolink:is_molecular_consequence_of"
    is_nearby_variant_of = "biolink:is_nearby_variant_of"
    is_non_coding_variant_of = "biolink:is_non_coding_variant_of"
    is_nonsense_variant_of = "biolink:is_nonsense_variant_of"
    is_output_of = "biolink:is_output_of"
    is_sequence_variant_of = "biolink:is_sequence_variant_of"
    is_splice_site_variant_of = "biolink:is_splice_site_variant_of"
    is_substrate_of = "biolink:is_substrate_of"
    is_synonymous_variant_of = "biolink:is_synonymous_variant_of"
    lacks_part = "biolink:lacks_part"
    localization_affected_by = "biolink:localization_affected_by"
    localization_decreased_by = "biolink:localization_decreased_by"
    localization_increased_by = "biolink:localization_increased_by"
    located_in = "biolink:located_in"
    location_of = "biolink:location_of"
    manifestation_of = "biolink:manifestation_of"
    mentioned_by = "biolink:mentioned_by"
    mentions = "biolink:mentions"
    metabolic_processing_affected_by = "biolink:metabolic_processing_affected_by"
    metabolic_processing_decreased_by = "biolink:metabolic_processing_decreased_by"
    metabolic_processing_increased_by = "biolink:metabolic_processing_increased_by"
    missing_from = "biolink:missing_from"
    model_of = "biolink:model_of"
    models = "biolink:models"
    molecular_activity_enabled_by = "biolink:molecular_activity_enabled_by"
    molecular_activity_has_input = "biolink:molecular_activity_has_input"
    molecular_activity_has_output = "biolink:molecular_activity_has_output"
    molecular_interaction_decreased_by = "biolink:molecular_interaction_decreased_by"
    molecular_interaction_increased_by = "biolink:molecular_interaction_increased_by"
    molecular_modification_affected_by = "biolink:molecular_modification_affected_by"
    molecular_modification_decreased_by = "biolink:molecular_modification_decreased_by"
    molecular_modification_increased_by = "biolink:molecular_modification_increased_by"
    molecularly_interacts_with = "biolink:molecularly_interacts_with"
    mutation_rate_affected_by = "biolink:mutation_rate_affected_by"
    mutation_rate_decreased_by = "biolink:mutation_rate_decreased_by"
    mutation_rate_increased_by = "biolink:mutation_rate_increased_by"
    narrow_match = "biolink:narrow_match"
    negatively_correlated_with = "biolink:negatively_correlated_with"
    not_completed_by = "biolink:not_completed_by"
    nutrient_of = "biolink:nutrient_of"
    occurs_in = "biolink:occurs_in"
    occurs_together_in_literature_with = "biolink:occurs_together_in_literature_with"
    opposite_of = "biolink:opposite_of"
    orthologous_to = "biolink:orthologous_to"
    overlaps = "biolink:overlaps"
    paralogous_to = "biolink:paralogous_to"
    part_of = "biolink:part_of"
    participates_in = "biolink:participates_in"
    phenotype_of = "biolink:phenotype_of"
    physically_interacts_with = "biolink:physically_interacts_with"
    plasma_membrane_part_of = "biolink:plasma_membrane_part_of"
    positively_correlated_with = "biolink:positively_correlated_with"
    preceded_by = "biolink:preceded_by"
    precedes = "biolink:precedes"
    predisposes = "biolink:predisposes"
    prevented_by = "biolink:prevented_by"
    prevents = "biolink:prevents"
    process_negatively_regulated_by_process = "biolink:process_negatively_regulated_by_process"
    process_negatively_regulates_process = "biolink:process_negatively_regulates_process"
    process_positively_regulated_by_process = "biolink:process_positively_regulated_by_process"
    process_positively_regulates_process = "biolink:process_positively_regulates_process"
    process_regulated_by_process = "biolink:process_regulated_by_process"
    process_regulates_process = "biolink:process_regulates_process"
    produced_by = "biolink:produced_by"
    produces = "biolink:produces"
    provider = "biolink:provider"
    publisher = "biolink:publisher"
    related_condition = "biolink:related_condition"
    related_to = "biolink:related_to"
    related_to_at_concept_level = "biolink:related_to_at_concept_level"
    related_to_at_instance_level = "biolink:related_to_at_instance_level"
    resistance_associated_with = "biolink:resistance_associated_with"
    response_affected_by = "biolink:response_affected_by"
    response_decreased_by = "biolink:response_decreased_by"
    response_increased_by = "biolink:response_increased_by"
    risk_affected_by = "biolink:risk_affected_by"
    same_as = "biolink:same_as"
    secretion_affected_by = "biolink:secretion_affected_by"
    secretion_decreased_by = "biolink:secretion_decreased_by"
    secretion_increased_by = "biolink:secretion_increased_by"
    sensitivity_associated_with = "biolink:sensitivity_associated_with"
    sequence_location_of = "biolink:sequence_location_of"
    similar_to = "biolink:similar_to"
    splicing_affected_by = "biolink:splicing_affected_by"
    splicing_decreased_by = "biolink:splicing_decreased_by"
    splicing_increased_by = "biolink:splicing_increased_by"
    stability_affected_by = "biolink:stability_affected_by"
    stability_decreased_by = "biolink:stability_decreased_by"
    stability_increased_by = "biolink:stability_increased_by"
    subclass_of = "biolink:subclass_of"
    superclass_of = "biolink:superclass_of"
    synthesis_affected_by = "biolink:synthesis_affected_by"
    synthesis_decreased_by = "biolink:synthesis_decreased_by"
    synthesis_increased_by = "biolink:synthesis_increased_by"
    target_for = "biolink:target_for"
    taxon_of = "biolink:taxon_of"
    temporally_related_to = "biolink:temporally_related_to"
    transcribed_from = "biolink:transcribed_from"
    transcribed_to = "biolink:transcribed_to"
    translates_to = "biolink:translates_to"
    translation_of = "biolink:translation_of"
    transport_affected_by = "biolink:transport_affected_by"
    transport_decreased_by = "biolink:transport_decreased_by"
    transport_increased_by = "biolink:transport_increased_by"
    treated_by = "biolink:treated_by"
    treats = "biolink:treats"
    uptake_affected_by = "biolink:uptake_affected_by"
    uptake_decreased_by = "biolink:uptake_decreased_by"
    uptake_increased_by = "biolink:uptake_increased_by"
    variant_part_of = "biolink:variant_part_of"
    xenologous_to = "biolink:xenologous_to"


Predicate = namedtuple(
    'biolink_predicate', [pred.value.replace('biolink:', '') for pred in PredicateType]
)(*[pred.value for pred in PredicateType])


# Enumerations
@unique
class LogicalInterpretationEnum(str, Enum):

    SomeSome = "SomeSome"
    AllSome = "AllSome"
    InverseAllSome = "InverseAllSome"


@unique
class ReactionDirectionEnum(str, Enum):

    left_to_right = "left_to_right"
    right_to_left = "right_to_left"
    bidirectional = "bidirectional"
    neutral = "neutral"


@unique
class ReactionSideEnum(str, Enum):

    left = "left"
    right = "right"


@unique
class PhaseEnum(str, Enum):
    """
    phase
    """

    value_0 = "0"
    value_1 = "1"
    value_2 = "2"


@unique
class StrandEnum(str, Enum):
    """
    strand
    """

    value_0 = "+"
    value_1 = "-"
    value_2 = "."
    value_3 = "?"


@unique
class SequenceEnum(str, Enum):
    """
    type of sequence
    """

    NA = "NA"
    AA = "AA"


@unique
class PredicateQualifierEnum(str, Enum):
    """
    constrained list of qualifying terms that soften or expand the definition of the predicate used. can be used to
    constrain or qualify any predicate (any child of related_to).
    """

    predicted = "predicted"
    possibly = "possibly"
    hypothesized = "hypothesized"
    validated = "validated"
    value_4 = "supported by real-world evidence"
    value_5 = "supported by clinical evidence"


@unique
class DruggableGeneCategoryEnum(str, Enum):

    Tclin = "Tclin"
    Tbio = "Tbio"
    Tchem = "Tchem"
    Tdark = "Tdark"


@unique
class DrugAvailabilityEnum(str, Enum):

    value_0 = "over the counter"
    prescription = "prescription"


@unique
class DrugDeliveryEnum(str, Enum):

    inhalation = "inhalation"
    oral = "oral"
    value_2 = "absorbtion through the skin"
    value_3 = "intravenous injection"


@unique
class FDAApprovalStatusEnum(str, Enum):

    value_0 = "Discovery & Development Phase"
    value_1 = "Preclinical Research Phase"
    value_2 = "FDA Clinical Research Phase"
    value_3 = "FDA Review Phase 4"
    value_4 = "FDA Post-Market Safety Monitoring"
    value_5 = "FDA Clinical Research Phase 1"
    value_6 = "FDA Clinical Research Phase 2"
    value_7 = "FDA Clinical Research Phase 3"
    value_8 = "FDA Clinical Research Phase 4"
    value_9 = "FDA Fast Track"
    value_10 = "FDA Breakthrough Therapy"
    value_11 = "FDA Accelerated Approval"
    value_12 = "FDA Priority Review"
    value_13 = "Regular FDA Approval"
    value_14 = "Post-Approval Withdrawal"


# Classes


@dataclass(config=PydanticConfig)
class OntologyClass:
    """
    a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be
    considered both instances of biolink classes, and OWL classes in their own right. In general you should not need
    to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of
    endocytosis (GO:0006897), use bl:BiologicalProcess as the type.
    """

    # Class Variables
    _id_prefixes: ClassVar[List[str]] = ["MESH", "UMLS", "KEGG.BRITE"]


@dataclass(config=PydanticConfig)
class Annotation:
    """
    Biolink Model root class for entity annotations.
    """


@dataclass(config=PydanticConfig)
class QuantityValue(Annotation):
    """
    A value of an attribute that is quantitative and measurable, expressed as a combination of a unit and a numeric
    value
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:QuantityValue"}

    has_unit: Optional[Union[str, Unit]] = None
    has_numeric_value: Optional[Union[float, float]] = None


@dataclass(config=PydanticConfig)
class Attribute(Annotation, OntologyClass):
    """
    A property or characteristic of an entity. For example, an apple may have properties such as color, shape, age,
    crispiness. An environmental sample may have attributes such as depth, lat, long, material.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Attribute"}
    _id_prefixes: ClassVar[List[str]] = ["EDAM-DATA", "EDAM-FORMAT", "EDAM-OPERATION", "EDAM-TOPIC"]

    has_attribute_type: Union[str, OntologyClass] = None
    name: Optional[Union[str, LabelType]] = None
    has_quantitative_value: Optional[
        Union[List[Union[str, QuantityValue]], Union[str, QuantityValue]]
    ] = field(default_factory=list)
    has_qualitative_value: Optional[Union[URIorCURIE, NamedThing]] = None
    iri: Optional[IriType] = None
    source: Optional[Union[str, str]] = None

    # Validators

    @validator('has_attribute_type', allow_reuse=True)
    def validate_required_has_attribute_type(cls, value):
        check_value_is_not_none("has_attribute_type", value)
        return value

    @validator('has_quantitative_value', allow_reuse=True)
    def convert_has_quantitative_value_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    @validator('has_qualitative_value', allow_reuse=True)
    def check_has_qualitative_value_prefix(cls, value):
        check_curie_prefix(NamedThing, value)
        return value


@dataclass(config=PydanticConfig)
class ChemicalRole(Attribute):

    # Class Variables
    category: ClassVar[str] = {"biolink:ChemicalRole"}


@dataclass(config=PydanticConfig)
class BiologicalSex(Attribute):

    # Class Variables
    category: ClassVar[str] = {"biolink:BiologicalSex"}


@dataclass(config=PydanticConfig)
class PhenotypicSex(BiologicalSex):
    """
    An attribute corresponding to the phenotypic sex of the individual, based upon the reproductive organs present.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PhenotypicSex"}


@dataclass(config=PydanticConfig)
class GenotypicSex(BiologicalSex):
    """
    An attribute corresponding to the genotypic sex of the individual, based upon genotypic composition of sex
    chromosomes.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GenotypicSex"}


@dataclass(config=PydanticConfig)
class SeverityValue(Attribute):
    """
    describes the severity of a phenotypic feature or disease
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:SeverityValue"}


@dataclass(config=PydanticConfig)
class RelationshipQuantifier:

    pass


@dataclass(config=PydanticConfig)
class SensitivityQuantifier(RelationshipQuantifier):

    pass


@dataclass(config=PydanticConfig)
class SpecificityQuantifier(RelationshipQuantifier):

    pass


@dataclass(config=PydanticConfig)
class PathognomonicityQuantifier(SpecificityQuantifier):
    """
    A relationship quantifier between a variant or symptom and a disease, which is high when the presence of the
    feature implies the existence of the disease
    """


@dataclass(config=PydanticConfig)
class FrequencyQuantifier(RelationshipQuantifier):
    has_count: Optional[Union[int, int]] = None
    has_total: Optional[Union[int, int]] = None
    has_quotient: Optional[Union[float, float]] = None
    has_percentage: Optional[Union[float, float]] = None


@dataclass(config=PydanticConfig)
class ChemicalOrDrugOrTreatment:

    pass


@dataclass(config=PydanticConfig)
class Entity:
    """
    Root Biolink Model class for all things and informational relationships, real or imagined.
    """

    id: Union[URIorCURIE, Entity] = None
    iri: Optional[IriType] = None
    category: Optional[Union[List[Union[str, CategoryType]], Union[str, CategoryType]]] = field(
        default_factory=list
    )
    type: Optional[Union[str, str]] = None
    name: Optional[Union[str, LabelType]] = None
    description: Optional[Union[str, NarrativeText]] = None
    source: Optional[Union[str, str]] = None
    has_attribute: Optional[Union[List[Union[str, Attribute]], Union[str, Attribute]]] = field(
        default_factory=list
    )

    # Validators

    @validator('id', allow_reuse=True)
    def validate_required_id(cls, value):
        check_value_is_not_none("id", value)
        check_curie_prefix(Entity, value)
        return value

    @validator('has_attribute', allow_reuse=True)
    def convert_has_attribute_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    def __post_init__(self):
        # Initialize default categories if not set
        # by traversing the MRO chain
        pass
        # if not self.category:
        #     self.category = list(
        #         {
        #             f'biolink:{super_class._category}'
        #             for super_class in inspect.getmro(type(self))
        #             if hasattr(super_class, '_category')
        #         }
        #     )


@dataclass(config=PydanticConfig)
class NamedThing(Entity):
    """
    a databased entity or concept/class
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:NamedThing"}

    category: Union[List[Union[URIorCURIE, NamedThing]], Union[URIorCURIE, NamedThing]] = None
    provided_by: Optional[Union[List[Union[str, str]], Union[str, str]]] = field(
        default_factory=list
    )

    # Validators

    @validator('provided_by', allow_reuse=True)
    def convert_provided_by_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)


@dataclass(config=PydanticConfig)
class RelationshipType(OntologyClass):
    """
    An OWL property used as an edge label
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:RelationshipType"}


@dataclass(config=PydanticConfig)
class GeneOntologyClass(OntologyClass):
    """
    an ontology class that describes a functional aspect of a gene, gene prodoct or complex
    """


@dataclass(config=PydanticConfig)
class UnclassifiedOntologyClass(OntologyClass):
    """
    this is used for nodes that are taken from an ontology but are not typed using an existing biolink class
    """


@dataclass(config=PydanticConfig)
class TaxonomicRank(OntologyClass):
    """
    A descriptor for the rank within a taxonomic classification. Example instance: TAXRANK:0000017 (kingdom)
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:TaxonomicRank"}
    _id_prefixes: ClassVar[List[str]] = ["TAXRANK"]


@dataclass(config=PydanticConfig)
class OrganismTaxon(NamedThing):
    """
    A classification of a set of organisms. Example instances: NCBITaxon:9606 (Homo sapiens), NCBITaxon:2 (Bacteria).
    Can also be used to represent strains or subspecies.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:OrganismTaxon"}
    _id_prefixes: ClassVar[List[str]] = ["NCBITaxon", "MESH"]

    has_taxonomic_rank: Optional[Union[str, TaxonomicRank]] = None


@dataclass(config=PydanticConfig)
class Event(NamedThing):
    """
    Something that happens at a given place and time.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Event"}


@dataclass(config=PydanticConfig)
class AdministrativeEntity(NamedThing):

    pass


@dataclass(config=PydanticConfig)
class Agent(AdministrativeEntity):
    """
    person, group, organization or project that provides a piece of information (i.e. a knowledge association)
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Agent"}
    _id_prefixes: ClassVar[List[str]] = ["isbn", "ORCID", "ScopusID", "ResearchID", "GSID", "isni"]

    id: Union[URIorCURIE, Agent] = None
    affiliation: Optional[Union[List[Union[str, URIorCURIE]], Union[str, URIorCURIE]]] = field(
        default_factory=list
    )
    address: Optional[Union[str, str]] = None
    name: Optional[Union[str, LabelType]] = None

    # Validators

    @validator('affiliation', allow_reuse=True)
    def convert_affiliation_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    @validator('id', allow_reuse=True)
    def validate_required_id(cls, value):
        check_value_is_not_none("id", value)
        check_curie_prefix(Agent, value)
        return value


@dataclass(config=PydanticConfig)
class InformationContentEntity(NamedThing):
    """
    a piece of information that typically describes some topic of discourse or is used as support.
    """

    # Class Variables
    _id_prefixes: ClassVar[List[str]] = ["doi"]

    license: Optional[Union[str, str]] = None
    rights: Optional[Union[str, str]] = None
    format: Optional[Union[str, str]] = None
    creation_date: Optional[Union[str, XSDDate]] = None


@dataclass(config=PydanticConfig)
class Dataset(InformationContentEntity):
    """
    an item that refers to a collection of data from a data source.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Dataset"}


@dataclass(config=PydanticConfig)
class DatasetDistribution(InformationContentEntity):
    """
    an item that holds distribution level information about a dataset.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:DatasetDistribution"}

    distribution_download_url: Optional[Union[str, str]] = None


@dataclass(config=PydanticConfig)
class DatasetVersion(InformationContentEntity):
    """
    an item that holds version level information about a dataset.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:DatasetVersion"}

    has_dataset: Optional[Union[URIorCURIE, Dataset]] = None
    ingest_date: Optional[Union[str, str]] = None
    has_distribution: Optional[Union[URIorCURIE, DatasetDistribution]] = None

    # Validators

    @validator('has_dataset', allow_reuse=True)
    def check_has_dataset_prefix(cls, value):
        check_curie_prefix(Dataset, value)
        return value

    @validator('has_distribution', allow_reuse=True)
    def check_has_distribution_prefix(cls, value):
        check_curie_prefix(DatasetDistribution, value)
        return value


@dataclass(config=PydanticConfig)
class DatasetSummary(InformationContentEntity):
    """
    an item that holds summary level information about a dataset.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:DatasetSummary"}

    source_web_page: Optional[Union[str, str]] = None
    source_logo: Optional[Union[str, str]] = None


@dataclass(config=PydanticConfig)
class ConfidenceLevel(InformationContentEntity):
    """
    Level of confidence in a statement
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ConfidenceLevel"}


@dataclass(config=PydanticConfig)
class EvidenceType(InformationContentEntity):
    """
    Class of evidence that supports an association
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:EvidenceType"}


@dataclass(config=PydanticConfig)
class InformationResource(InformationContentEntity):
    """
    A database or knowledgebase and its supporting ecosystem of interfaces and services that deliver content to
    consumers (e.g. web portals, APIs, query endpoints, streaming services, data downloads, etc.). A single
    Information Resource by this definition may span many different datasets or databases, and include many access
    endpoints and user interfaces. Information Resources include project-specific resources such as a Translator
    Knowledge Provider, and community knowledgebases like ChemBL, OMIM, or DGIdb.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:InformationResource"}


@dataclass(config=PydanticConfig)
class Publication(InformationContentEntity):
    """
    Any published piece of information. Can refer to a whole publication, its encompassing publication (i.e. journal
    or book) or to a part of a publication, if of significant knowledge scope (e.g. a figure, figure legend, or
    section highlighted by NLP). The scope is intended to be general and include information published on the web, as
    well as printed materials, either directly or in one of the Publication Biolink category subclasses.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Publication"}
    _id_prefixes: ClassVar[List[str]] = ["NLMID"]

    id: Union[URIorCURIE, Publication] = None
    type: Union[str, str] = None
    authors: Optional[Union[List[Union[str, str]], Union[str, str]]] = field(default_factory=list)
    pages: Optional[Union[List[Union[str, str]], Union[str, str]]] = field(default_factory=list)
    summary: Optional[Union[str, str]] = None
    keywords: Optional[Union[List[Union[str, str]], Union[str, str]]] = field(default_factory=list)
    mesh_terms: Optional[Union[List[Union[str, URIorCURIE]], Union[str, URIorCURIE]]] = field(
        default_factory=list
    )
    xref: Optional[Union[List[Union[str, URIorCURIE]], Union[str, URIorCURIE]]] = field(
        default_factory=list
    )
    name: Optional[Union[str, LabelType]] = None

    # Validators

    @validator('authors', allow_reuse=True)
    def convert_authors_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    @validator('pages', allow_reuse=True)
    def convert_pages_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    @validator('keywords', allow_reuse=True)
    def convert_keywords_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    @validator('mesh_terms', allow_reuse=True)
    def convert_mesh_terms_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    @validator('xref', allow_reuse=True)
    def convert_xref_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    @validator('id', allow_reuse=True)
    def validate_required_id(cls, value):
        check_value_is_not_none("id", value)
        check_curie_prefix(Publication, value)
        return value

    @validator('type', allow_reuse=True)
    def validate_required_type(cls, value):
        check_value_is_not_none("type", value)
        return value


@dataclass(config=PydanticConfig)
class Book(Publication):
    """
    This class may rarely be instantiated except if use cases of a given knowledge graph support its utility.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Book"}
    _id_prefixes: ClassVar[List[str]] = ["isbn", "NLMID"]

    id: Union[URIorCURIE, Book] = None
    type: Union[str, str] = None

    # Validators

    @validator('id', allow_reuse=True)
    def validate_required_id(cls, value):
        check_value_is_not_none("id", value)
        check_curie_prefix(Book, value)
        return value

    @validator('type', allow_reuse=True)
    def validate_required_type(cls, value):
        check_value_is_not_none("type", value)
        return value


@dataclass(config=PydanticConfig)
class BookChapter(Publication):

    # Class Variables
    category: ClassVar[str] = {"biolink:BookChapter"}

    published_in: Union[str, URIorCURIE] = None
    volume: Optional[Union[str, str]] = None
    chapter: Optional[Union[str, str]] = None

    # Validators

    @validator('published_in', allow_reuse=True)
    def validate_required_published_in(cls, value):
        check_value_is_not_none("published_in", value)
        return value


@dataclass(config=PydanticConfig)
class Serial(Publication):
    """
    This class may rarely be instantiated except if use cases of a given knowledge graph support its utility.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Serial"}
    _id_prefixes: ClassVar[List[str]] = ["issn", "NLMID"]

    id: Union[URIorCURIE, Serial] = None
    type: Union[str, str] = None
    iso_abbreviation: Optional[Union[str, str]] = None
    volume: Optional[Union[str, str]] = None
    issue: Optional[Union[str, str]] = None

    # Validators

    @validator('id', allow_reuse=True)
    def validate_required_id(cls, value):
        check_value_is_not_none("id", value)
        check_curie_prefix(Serial, value)
        return value

    @validator('type', allow_reuse=True)
    def validate_required_type(cls, value):
        check_value_is_not_none("type", value)
        return value


@dataclass(config=PydanticConfig)
class Article(Publication):

    # Class Variables
    category: ClassVar[str] = {"biolink:Article"}
    _id_prefixes: ClassVar[List[str]] = ["PMID"]

    published_in: Union[str, URIorCURIE] = None
    iso_abbreviation: Optional[Union[str, str]] = None
    volume: Optional[Union[str, str]] = None
    issue: Optional[Union[str, str]] = None

    # Validators

    @validator('published_in', allow_reuse=True)
    def validate_required_published_in(cls, value):
        check_value_is_not_none("published_in", value)
        return value


@dataclass(config=PydanticConfig)
class PhysicalEssenceOrOccurrent:
    """
    Either a physical or processual entity.
    """


@dataclass(config=PydanticConfig)
class PhysicalEssence(PhysicalEssenceOrOccurrent):
    """
    Semantic mixin concept.  Pertains to entities that have physical properties such as mass, volume, or charge.
    """


@dataclass(config=PydanticConfig)
class PhysicalEntity(NamedThing, PhysicalEssence):
    """
    An entity that has material reality (a.k.a. physical essence).
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PhysicalEntity"}


@dataclass(config=PydanticConfig)
class Occurrent(PhysicalEssenceOrOccurrent):
    """
    A processual entity.
    """


@dataclass(config=PydanticConfig)
class ActivityAndBehavior(Occurrent):
    """
    Activity or behavior of any independent integral living, organization or mechanical actor in the world
    """


@dataclass(config=PydanticConfig)
class Activity(NamedThing, ActivityAndBehavior):
    """
    An activity is something that occurs over a period of time and acts upon or with entities; it may include
    consuming, processing, transforming, modifying, relocating, using, or generating entities.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Activity"}


@dataclass(config=PydanticConfig)
class Procedure(NamedThing, ActivityAndBehavior):
    """
    A series of actions conducted in a certain order or manner
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Procedure"}
    _id_prefixes: ClassVar[List[str]] = ["CPT"]


@dataclass(config=PydanticConfig)
class Phenomenon(NamedThing, Occurrent):
    """
    a fact or situation that is observed to exist or happen, especially one whose cause or explanation is in question
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Phenomenon"}


@dataclass(config=PydanticConfig)
class Device(NamedThing):
    """
    A thing made or adapted for a particular purpose, especially a piece of mechanical or electronic equipment
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Device"}


@dataclass(config=PydanticConfig)
class SubjectOfInvestigation:
    """
    An entity that has the role of being studied in an investigation, study, or experiment
    """


@dataclass(config=PydanticConfig)
class MaterialSample(PhysicalEntity, SubjectOfInvestigation):
    """
    A sample is a limited quantity of something (e.g. an individual or set of individuals from a population, or a
    portion of a substance) to be used for testing, analysis, inspection, investigation, demonstration, or trial use.
    [SIO]
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:MaterialSample"}
    _id_prefixes: ClassVar[List[str]] = ["BIOSAMPLE", "GOLD.META"]


@dataclass(config=PydanticConfig)
class PlanetaryEntity(NamedThing):
    """
    Any entity or process that exists at the level of the whole planet
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PlanetaryEntity"}


@dataclass(config=PydanticConfig)
class EnvironmentalProcess(PlanetaryEntity, Occurrent):

    # Class Variables
    category: ClassVar[str] = {"biolink:EnvironmentalProcess"}


@dataclass(config=PydanticConfig)
class EnvironmentalFeature(PlanetaryEntity):

    # Class Variables
    category: ClassVar[str] = {"biolink:EnvironmentalFeature"}


@dataclass(config=PydanticConfig)
class GeographicLocation(PlanetaryEntity):
    """
    a location that can be described in lat/long coordinates
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GeographicLocation"}

    latitude: Optional[Union[float, float]] = None
    longitude: Optional[Union[float, float]] = None


@dataclass(config=PydanticConfig)
class GeographicLocationAtTime(GeographicLocation):
    """
    a location that can be described in lat/long coordinates, for a particular time
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GeographicLocationAtTime"}

    timepoint: Optional[Union[str, TimeType]] = None


@dataclass(config=PydanticConfig)
class BiologicalEntity(NamedThing):

    pass


@dataclass(config=PydanticConfig)
class ThingWithTaxon:
    """
    A mixin that can be used on any entity that can be taxonomically classified. This includes individual organisms;
    genes, their products and other molecular entities; body parts; biological processes
    """

    in_taxon: Optional[
        Union[List[Union[URIorCURIE, OrganismTaxon]], Union[URIorCURIE, OrganismTaxon]]
    ] = field(default_factory=list)

    # Validators

    @validator('in_taxon', allow_reuse=True)
    def convert_in_taxon_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(OrganismTaxon, value)


@dataclass(config=PydanticConfig)
class GenomicEntity(ThingWithTaxon):
    has_biological_sequence: Optional[Union[str, BiologicalSequence]] = None


@dataclass(config=PydanticConfig)
class ChemicalSubstance:

    # Class Variables
    category: ClassVar[str] = {"biolink:ChemicalSubstance"}


@dataclass(config=PydanticConfig)
class BiologicalProcessOrActivity(BiologicalEntity, Occurrent, OntologyClass):
    """
    Either an individual molecular activity, or a collection of causally connected molecular activities in a
    biological system.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:BiologicalProcessOrActivity"}
    _id_prefixes: ClassVar[List[str]] = ["GO", "REACT"]

    has_input: Optional[
        Union[
            List[Union[URIorCURIE, BiologicalProcessOrActivity]],
            Union[URIorCURIE, BiologicalProcessOrActivity],
        ]
    ] = field(default_factory=list)
    has_output: Optional[
        Union[
            List[Union[URIorCURIE, BiologicalProcessOrActivity]],
            Union[URIorCURIE, BiologicalProcessOrActivity],
        ]
    ] = field(default_factory=list)
    enabled_by: Optional[
        Union[List[Union[URIorCURIE, PhysicalEntity]], Union[URIorCURIE, PhysicalEntity]]
    ] = field(default_factory=list)

    # Validators

    @validator('has_input', allow_reuse=True)
    def convert_has_input_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(BiologicalProcessOrActivity, value)

    @validator('has_output', allow_reuse=True)
    def convert_has_output_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(BiologicalProcessOrActivity, value)

    @validator('enabled_by', allow_reuse=True)
    def convert_enabled_by_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(PhysicalEntity, value)


@dataclass(config=PydanticConfig)
class MolecularActivity(BiologicalProcessOrActivity, Occurrent, OntologyClass):
    """
    An execution of a molecular function carried out by a gene product or macromolecular complex.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:MolecularActivity"}
    _id_prefixes: ClassVar[List[str]] = [
        "GO",
        "REACT",
        "RHEA",
        "metacyc.reaction",
        "EC",
        "TCDB",
        "KEGG.REACTION",
        "KEGG.RCLASS",
        "KEGG.ENZYME",
        "KEGG.ORTHOLOGY",
        "UMLS",
        "BIGG.REACTION",
        "SEED.REACTION",
        "METANETX.REACTION",
    ]

    has_input: Optional[
        Union[List[Union[URIorCURIE, MolecularEntity]], Union[URIorCURIE, MolecularEntity]]
    ] = field(default_factory=list)
    has_output: Optional[
        Union[List[Union[URIorCURIE, MolecularEntity]], Union[URIorCURIE, MolecularEntity]]
    ] = field(default_factory=list)
    enabled_by: Optional[
        Union[List[Union[str, MacromolecularMachineMixin]], Union[str, MacromolecularMachineMixin]]
    ] = field(default_factory=list)

    # Validators

    @validator('has_input', allow_reuse=True)
    def convert_has_input_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(MolecularEntity, value)

    @validator('has_output', allow_reuse=True)
    def convert_has_output_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(MolecularEntity, value)

    @validator('enabled_by', allow_reuse=True)
    def convert_enabled_by_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)


@dataclass(config=PydanticConfig)
class BiologicalProcess(BiologicalProcessOrActivity, Occurrent, OntologyClass):
    """
    One or more causally connected executions of molecular functions
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:BiologicalProcess"}
    _id_prefixes: ClassVar[List[str]] = ["GO", "REACT", "metacyc.reaction", "KEGG.MODULE"]


@dataclass(config=PydanticConfig)
class Pathway(BiologicalProcess, OntologyClass):

    # Class Variables
    category: ClassVar[str] = {"biolink:Pathway"}
    _id_prefixes: ClassVar[List[str]] = [
        "GO",
        "REACT",
        "KEGG",
        "SMPDB",
        "MSigDB",
        "PHARMGKB.PATHWAYS",
        "WIKIPATHWAYS",
        "FB",
        "PANTHER.PATHWAY",
        "KEGG.PATHWAY",
    ]


@dataclass(config=PydanticConfig)
class PhysiologicalProcess(BiologicalProcess, OntologyClass):

    # Class Variables
    category: ClassVar[str] = {"biolink:PhysiologicalProcess"}
    _id_prefixes: ClassVar[List[str]] = ["GO", "REACT"]


@dataclass(config=PydanticConfig)
class Behavior(BiologicalProcess, ActivityAndBehavior, OntologyClass):

    # Class Variables
    category: ClassVar[str] = {"biolink:Behavior"}


@dataclass(config=PydanticConfig)
class OrganismAttribute(Attribute):
    """
    describes a characteristic of an organismal entity.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:OrganismAttribute"}


@dataclass(config=PydanticConfig)
class PhenotypicQuality(OrganismAttribute):
    """
    A property of a phenotype
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PhenotypicQuality"}


@dataclass(config=PydanticConfig)
class Inheritance(OrganismAttribute):
    """
    The pattern or 'mode' in which a particular genetic trait or disorder is passed from one generation to the next,
    e.g. autosomal dominant, autosomal recessive, etc.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Inheritance"}


@dataclass(config=PydanticConfig)
class OrganismalEntity(BiologicalEntity):
    """
    A named entity that is either a part of an organism, a whole organism, population or clade of organisms, excluding
    chemical entities
    """

    has_attribute: Optional[Union[List[Union[str, Attribute]], Union[str, Attribute]]] = field(
        default_factory=list
    )

    # Validators

    @validator('has_attribute', allow_reuse=True)
    def convert_has_attribute_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)


@dataclass(config=PydanticConfig)
class LifeStage(OrganismalEntity, ThingWithTaxon):
    """
    A stage of development or growth of an organism, including post-natal adult stages
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:LifeStage"}
    _id_prefixes: ClassVar[List[str]] = ["HsapDv", "MmusDv", "ZFS", "FBdv", "WBls", "UBERON"]


@dataclass(config=PydanticConfig)
class IndividualOrganism(OrganismalEntity, ThingWithTaxon):
    """
    An instance of an organism. For example, Richard Nixon, Charles Darwin, my pet cat. Example ID:
    ORCID:0000-0002-5355-2576
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:IndividualOrganism"}
    _id_prefixes: ClassVar[List[str]] = ["ORCID"]


@dataclass(config=PydanticConfig)
class PopulationOfIndividualOrganisms(OrganismalEntity, ThingWithTaxon):
    """
    A collection of individuals from the same taxonomic class distinguished by one or more characteristics.
    Characteristics can include, but are not limited to, shared geographic location, genetics, phenotypes.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PopulationOfIndividualOrganisms"}
    _id_prefixes: ClassVar[List[str]] = ["HANCESTRO"]


@dataclass(config=PydanticConfig)
class StudyPopulation(PopulationOfIndividualOrganisms):
    """
    A group of people banded together or treated as a group as participants in a research study.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:StudyPopulation"}


@dataclass(config=PydanticConfig)
class DiseaseOrPhenotypicFeature(BiologicalEntity, ThingWithTaxon):
    """
    Either one of a disease or an individual phenotypic feature. Some knowledge resources such as Monarch treat these
    as distinct, others such as MESH conflate.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:DiseaseOrPhenotypicFeature"}


@dataclass(config=PydanticConfig)
class Disease(DiseaseOrPhenotypicFeature):

    # Class Variables
    category: ClassVar[str] = {"biolink:Disease"}
    _id_prefixes: ClassVar[List[str]] = [
        "MONDO",
        "DOID",
        "OMIM",
        "OMIM.PS",
        "ORPHANET",
        "EFO",
        "UMLS",
        "MESH",
        "MEDDRA",
        "NCIT",
        "SNOMEDCT",
        "medgen",
        "ICD10",
        "ICD9",
        "KEGG.DISEASE",
        "HP",
        "MP",
    ]


@dataclass(config=PydanticConfig)
class PhenotypicFeature(DiseaseOrPhenotypicFeature):
    """
    A combination of entity and quality that makes up a phenotyping statement.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PhenotypicFeature"}
    _id_prefixes: ClassVar[List[str]] = [
        "HP",
        "EFO",
        "NCIT",
        "UMLS",
        "MEDDRA",
        "MP",
        "ZP",
        "UPHENO",
        "APO",
        "FBcv",
        "WBPhenotype",
        "SNOMEDCT",
        "MESH",
        "XPO",
        "FYPO",
        "TO",
    ]


@dataclass(config=PydanticConfig)
class BehavioralFeature(PhenotypicFeature):
    """
    A phenotypic feature which is behavioral in nature.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:BehavioralFeature"}


@dataclass(config=PydanticConfig)
class AnatomicalEntity(OrganismalEntity, ThingWithTaxon, PhysicalEssence):
    """
    A subcellular location, cell type or gross anatomical part
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:AnatomicalEntity"}
    _id_prefixes: ClassVar[List[str]] = [
        "UBERON",
        "GO",
        "CL",
        "UMLS",
        "MESH",
        "NCIT",
        "EMAPA",
        "ZFA",
        "FBbt",
        "WBbt",
    ]


@dataclass(config=PydanticConfig)
class CellularComponent(AnatomicalEntity):
    """
    A location in or around a cell
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:CellularComponent"}
    _id_prefixes: ClassVar[List[str]] = ["GO", "MESH", "UMLS", "NCIT", "SNOMEDCT", "CL", "UBERON"]


@dataclass(config=PydanticConfig)
class Cell(AnatomicalEntity):

    # Class Variables
    category: ClassVar[str] = {"biolink:Cell"}
    _id_prefixes: ClassVar[List[str]] = ["CL", "PO", "UMLS", "NCIT", "MESH", "UBERON", "SNOMEDCT"]


@dataclass(config=PydanticConfig)
class CellLine(OrganismalEntity):

    # Class Variables
    category: ClassVar[str] = {"biolink:CellLine"}
    _id_prefixes: ClassVar[List[str]] = ["CLO"]


@dataclass(config=PydanticConfig)
class GrossAnatomicalStructure(AnatomicalEntity):

    # Class Variables
    category: ClassVar[str] = {"biolink:GrossAnatomicalStructure"}
    _id_prefixes: ClassVar[List[str]] = ["UBERON", "UMLS", "MESH", "NCIT", "PO", "FAO"]


@dataclass(config=PydanticConfig)
class ChemicalEntityOrGeneOrGeneProduct:
    """
    A union of chemical entities and children, and gene or gene product. This mixin is helpful to use when searching
    across chemical entities that must include genes and their children as chemical entities.
    """


@dataclass(config=PydanticConfig)
class ChemicalEntityOrProteinOrPolypeptide:
    """
    A union of chemical entities and children, and protein and polypeptide. This mixin is helpful to use when
    searching across chemical entities that must include genes and their children as chemical entities.
    """


@dataclass(config=PydanticConfig)
class ChemicalEntity(
    NamedThing,
    PhysicalEssence,
    ChemicalOrDrugOrTreatment,
    ChemicalEntityOrGeneOrGeneProduct,
    ChemicalEntityOrProteinOrPolypeptide,
):
    """
    A chemical entity is a physical entity that pertains to chemistry or biochemistry.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ChemicalEntity"}
    _id_prefixes: ClassVar[List[str]] = ["UNII", "MESH", "CAS", "UMLS"]

    trade_name: Optional[Union[URIorCURIE, ChemicalEntity]] = None
    available_from: Optional[
        Union[List[Union[str, DrugAvailabilityEnum]], Union[str, DrugAvailabilityEnum]]
    ] = field(default_factory=list)
    max_tolerated_dose: Optional[Union[str, str]] = None
    is_toxic: Optional[Union[bool, Bool]] = None
    has_chemical_role: Optional[
        Union[List[Union[str, ChemicalRole]], Union[str, ChemicalRole]]
    ] = field(default_factory=list)

    # Validators

    @validator('trade_name', allow_reuse=True)
    def check_trade_name_prefix(cls, value):
        check_curie_prefix(ChemicalEntity, value)
        return value

    @validator('available_from', allow_reuse=True)
    def convert_available_from_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    @validator('has_chemical_role', allow_reuse=True)
    def convert_has_chemical_role_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)


@dataclass(config=PydanticConfig)
class MolecularEntity(ChemicalEntity):
    """
    A molecular entity is a chemical entity composed of individual or covalently bonded atoms.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:MolecularEntity"}
    _id_prefixes: ClassVar[List[str]] = [
        "PUBCHEM.COMPOUND",
        "CHEMBL.COMPOUND",
        "UNII",
        "CHEBI",
        "DRUGBANK",
        "MESH",
        "CAS",
        "DrugCentral",
        "GTOPDB",
        "HMDB",
        "KEGG.COMPOUND",
        "ChemBank",
        "PUBCHEM.SUBSTANCE",
        "SIDER.DRUG",
        "INCHI",
        "INCHIKEY",
        "KEGG.GLYCAN",
        "KEGG.DRUG",
        "KEGG.DGROUP",
        "KEGG.ENVIRON",
        "UMLS",
    ]

    is_metabolite: Optional[Union[bool, Bool]] = None


@dataclass(config=PydanticConfig)
class SmallMolecule(MolecularEntity):
    """
    A small molecule entity is a molecular entity characterized by availability in small-molecule databases of SMILES,
    InChI, IUPAC, or other unambiguous representation of its precise chemical structure; for convenience of
    representation, any valid chemical representation is included, even if it is not strictly molecular (e.g., sodium
    ion).
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:SmallMolecule"}
    _id_prefixes: ClassVar[List[str]] = [
        "PUBCHEM.COMPOUND",
        "CHEMBL.COMPOUND",
        "UNII",
        "CHEBI",
        "DRUGBANK",
        "MESH",
        "CAS",
        "DrugCentral",
        "GTOPDB",
        "HMDB",
        "KEGG.COMPOUND",
        "ChemBank",
        "PUBCHEM.SUBSTANCE",
        "SIDER.DRUG",
        "INCHI",
        "INCHIKEY",
        "KEGG.GLYCAN",
        "KEGG.DRUG",
        "KEGG.DGROUP",
        "KEGG.ENVIRON",
        "BIGG.METABOLITE",
        "UMLS",
    ]

    id: Union[URIorCURIE, SmallMolecule] = None

    # Validators

    @validator('id', allow_reuse=True)
    def validate_required_id(cls, value):
        check_value_is_not_none("id", value)
        check_curie_prefix(SmallMolecule, value)
        return value


@dataclass(config=PydanticConfig)
class ChemicalMixture(ChemicalEntity):
    """
    A chemical mixture is a chemical entity composed of two or more molecular entities.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ChemicalMixture"}
    _id_prefixes: ClassVar[List[str]] = [
        "PUBCHEM.COMPOUND",
        "CHEMBL.COMPOUND",
        "UNII",
        "CHEBI",
        "DRUGBANK",
        "MESH",
        "CAS",
        "DrugCentral",
        "GTOPDB",
        "HMDB",
        "KEGG.COMPOUND",
        "ChemBank",
        "PUBCHEM.SUBSTANCE",
        "SIDER.DRUG",
        "INCHI",
        "INCHIKEY",
        "KEGG.GLYCAN",
        "KEGG.DRUG",
        "KEGG.DGROUP",
        "KEGG.ENVIRON",
        "UMLS",
    ]

    is_supplement: Optional[Union[URIorCURIE, ChemicalMixture]] = None
    highest_FDA_approval_status: Optional[Union[str, str]] = None
    drug_regulatory_status_world_wide: Optional[Union[str, str]] = None
    routes_of_delivery: Optional[
        Union[List[Union[str, DrugDeliveryEnum]], Union[str, DrugDeliveryEnum]]
    ] = field(default_factory=list)

    # Validators

    @validator('is_supplement', allow_reuse=True)
    def check_is_supplement_prefix(cls, value):
        check_curie_prefix(ChemicalMixture, value)
        return value

    @validator('routes_of_delivery', allow_reuse=True)
    def convert_routes_of_delivery_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)


@dataclass(config=PydanticConfig)
class NucleicAcidEntity(MolecularEntity, GenomicEntity, PhysicalEssence, OntologyClass):
    """
    A nucleic acid entity is a molecular entity characterized by availability in gene databases of nucleotide-based
    sequence representations of its precise sequence; for convenience of representation, partial sequences of various
    kinds are included.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:NucleicAcidEntity"}
    _id_prefixes: ClassVar[List[str]] = [
        "PUBCHEM.COMPOUND",
        "CHEMBL.COMPOUND",
        "UNII",
        "CHEBI",
        "MESH",
        "CAS",
        "GTOPDB",
        "HMDB",
        "KEGG.COMPOUND",
        "ChemBank",
        "PUBCHEM.SUBSTANCE",
        "INCHI",
        "INCHIKEY",
        "KEGG.GLYCAN",
        "KEGG.ENVIRON",
    ]


@dataclass(config=PydanticConfig)
class MolecularMixture(ChemicalMixture):
    """
    A molecular mixture is a chemical mixture composed of two or more molecular entities with known concentration and
    stoichiometry.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:MolecularMixture"}
    _id_prefixes: ClassVar[List[str]] = [
        "PUBCHEM.COMPOUND",
        "CHEMBL.COMPOUND",
        "UNII",
        "CHEBI",
        "DRUGBANK",
        "MESH",
        "CAS",
        "DrugCentral",
        "GTOPDB",
        "HMDB",
        "KEGG.COMPOUND",
        "ChemBank",
        "PUBCHEM.SUBSTANCE",
        "SIDER.DRUG",
        "INCHI",
        "INCHIKEY",
        "KEGG.GLYCAN",
        "KEGG.DRUG",
        "KEGG.DGROUP",
        "KEGG.ENVIRON",
        "UMLS",
    ]


@dataclass(config=PydanticConfig)
class ComplexMolecularMixture(ChemicalMixture):
    """
    A complex molecular mixture is a chemical mixture composed of two or more molecular entities with unknown
    concentration and stoichiometry.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ComplexMolecularMixture"}
    _id_prefixes: ClassVar[List[str]] = [
        "PUBCHEM.COMPOUND",
        "CHEMBL.COMPOUND",
        "UNII",
        "CHEBI",
        "DRUGBANK",
        "MESH",
        "CAS",
        "DrugCentral",
        "GTOPDB",
        "HMDB",
        "KEGG.COMPOUND",
        "ChemBank",
        "PUBCHEM.SUBSTANCE",
        "SIDER.DRUG",
        "INCHI",
        "INCHIKEY",
        "KEGG.GLYCAN",
        "KEGG.DRUG",
        "KEGG.DGROUP",
        "KEGG.ENVIRON",
        "UMLS",
    ]


@dataclass(config=PydanticConfig)
class ProcessedMaterial(ChemicalMixture):
    """
    A chemical entity (often a mixture) processed for consumption for nutritional, medical or technical use. Is a
    material entity that is created or changed during material processing.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ProcessedMaterial"}
    _id_prefixes: ClassVar[List[str]] = ["UMLS"]


@dataclass(config=PydanticConfig)
class Drug(MolecularMixture, ChemicalOrDrugOrTreatment, OntologyClass):
    """
    A substance intended for use in the diagnosis, cure, mitigation, treatment, or prevention of disease
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Drug"}
    _id_prefixes: ClassVar[List[str]] = ["RXCUI", "NDC", "UMLS"]


@dataclass(config=PydanticConfig)
class EnvironmentalFoodContaminant(ChemicalEntity):

    # Class Variables
    category: ClassVar[str] = {"biolink:EnvironmentalFoodContaminant"}


@dataclass(config=PydanticConfig)
class FoodAdditive(ChemicalEntity):

    # Class Variables
    category: ClassVar[str] = {"biolink:FoodAdditive"}


@dataclass(config=PydanticConfig)
class Nutrient(ChemicalEntity):

    # Class Variables
    category: ClassVar[str] = {"biolink:Nutrient"}


@dataclass(config=PydanticConfig)
class Macronutrient(Nutrient):

    # Class Variables
    category: ClassVar[str] = {"biolink:Macronutrient"}


@dataclass(config=PydanticConfig)
class Micronutrient(Nutrient):

    # Class Variables
    category: ClassVar[str] = {"biolink:Micronutrient"}


@dataclass(config=PydanticConfig)
class Vitamin(Micronutrient):

    # Class Variables
    category: ClassVar[str] = {"biolink:Vitamin"}


@dataclass(config=PydanticConfig)
class Food(ChemicalMixture):
    """
    A substance consumed by a living organism as a source of nutrition
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Food"}
    _id_prefixes: ClassVar[List[str]] = ["foodb.compound"]


@dataclass(config=PydanticConfig)
class MacromolecularMachineMixin:
    """
    A union of gene locus, gene product, and macromolecular complex mixin. These are the basic units of function in a
    cell. They either carry out individual biological activities, or they encode molecules which do this.
    """

    name: Optional[Union[str, SymbolType]] = None


@dataclass(config=PydanticConfig)
class GeneOrGeneProduct(MacromolecularMachineMixin):
    """
    A union of gene loci or gene products. Frequently an identifier for one will be used as proxy for another
    """

    # Class Variables
    _id_prefixes: ClassVar[List[str]] = ["CHEMBL.TARGET", "IUPHAR.FAMILY"]


@dataclass(config=PydanticConfig)
class Gene(
    BiologicalEntity,
    GeneOrGeneProduct,
    GenomicEntity,
    ChemicalEntityOrGeneOrGeneProduct,
    PhysicalEssence,
    OntologyClass,
):
    """
    A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A
    gene locus may include regulatory regions, transcribed regions and/or other functional sequence regions.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Gene"}
    _id_prefixes: ClassVar[List[str]] = [
        "NCBIGene",
        "ENSEMBL",
        "HGNC",
        "MGI",
        "ZFIN",
        "dictyBase",
        "WB",
        "WormBase",
        "FB",
        "RGD",
        "SGD",
        "PomBase",
        "OMIM",
        "KEGG.GENE",
        "UMLS",
        "Xenbase",
        "AspGD",
    ]

    symbol: Optional[Union[str, str]] = None
    synonym: Optional[Union[List[Union[str, LabelType]], Union[str, LabelType]]] = field(
        default_factory=list
    )
    xref: Optional[Union[List[Union[str, URIorCURIE]], Union[str, URIorCURIE]]] = field(
        default_factory=list
    )

    # Validators

    @validator('synonym', allow_reuse=True)
    def convert_synonym_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    @validator('xref', allow_reuse=True)
    def convert_xref_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)


@dataclass(config=PydanticConfig)
class GeneProductMixin(GeneOrGeneProduct):
    """
    The functional molecular product of a single gene locus. Gene products are either proteins or functional RNA
    molecules.
    """

    # Class Variables
    _id_prefixes: ClassVar[List[str]] = ["UniProtKB", "gtpo", "PR"]

    synonym: Optional[Union[List[Union[str, LabelType]], Union[str, LabelType]]] = field(
        default_factory=list
    )
    xref: Optional[Union[List[Union[str, URIorCURIE]], Union[str, URIorCURIE]]] = field(
        default_factory=list
    )

    # Validators

    @validator('synonym', allow_reuse=True)
    def convert_synonym_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    @validator('xref', allow_reuse=True)
    def convert_xref_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)


@dataclass(config=PydanticConfig)
class GeneProductIsoformMixin(GeneProductMixin):
    """
    This is an abstract class that can be mixed in with different kinds of gene products to indicate that the gene
    product is intended to represent a specific isoform rather than a canonical or reference or generic product. The
    designation of canonical or reference may be arbitrary, or it may represent the superclass of all isoforms.
    """


@dataclass(config=PydanticConfig)
class MacromolecularComplexMixin(MacromolecularMachineMixin):
    """
    A stable assembly of two or more macromolecules, i.e. proteins, nucleic acids, carbohydrates or lipids, in which
    at least one component is a protein and the constituent parts function together.
    """

    # Class Variables
    _id_prefixes: ClassVar[List[str]] = ["INTACT", "GO", "PR", "REACT"]


@dataclass(config=PydanticConfig)
class Genome(BiologicalEntity, GenomicEntity, PhysicalEssence, OntologyClass):
    """
    A genome is the sum of genetic material within a cell or virion.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Genome"}


@dataclass(config=PydanticConfig)
class Exon(NucleicAcidEntity):
    """
    A region of the transcript sequence within a gene which is not removed from the primary RNA transcript by RNA
    splicing.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Exon"}


@dataclass(config=PydanticConfig)
class Transcript(NucleicAcidEntity):
    """
    An RNA synthesized on a DNA or RNA template by an RNA polymerase.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Transcript"}
    _id_prefixes: ClassVar[List[str]] = ["ENSEMBL", "FB"]


@dataclass(config=PydanticConfig)
class CodingSequence(NucleicAcidEntity):

    # Class Variables
    category: ClassVar[str] = {"biolink:CodingSequence"}


@dataclass(config=PydanticConfig)
class Polypeptide(
    BiologicalEntity,
    ThingWithTaxon,
    ChemicalEntityOrGeneOrGeneProduct,
    ChemicalEntityOrProteinOrPolypeptide,
):
    """
    A polypeptide is a molecular entity characterized by availability in protein databases of amino-acid-based
    sequence representations of its precise primary structure; for convenience of representation, partial sequences of
    various kinds are included, even if they do not represent a physical molecule.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Polypeptide"}
    _id_prefixes: ClassVar[List[str]] = ["UniProtKB", "PR", "ENSEMBL", "FB", "UMLS"]


@dataclass(config=PydanticConfig)
class Protein(Polypeptide, GeneProductMixin, ThingWithTaxon):
    """
    A gene product that is composed of a chain of amino acid sequences and is produced by ribosome-mediated
    translation of mRNA
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Protein"}
    _id_prefixes: ClassVar[List[str]] = ["UniProtKB", "PR", "ENSEMBL", "FB", "UMLS", "MESH"]


@dataclass(config=PydanticConfig)
class ProteinIsoform(Protein, GeneProductIsoformMixin):
    """
    Represents a protein that is a specific isoform of the canonical or reference protein. See
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4114032/
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ProteinIsoform"}
    _id_prefixes: ClassVar[List[str]] = ["UniProtKB", "UNIPROT.ISOFORM", "PR", "ENSEMBL"]


@dataclass(config=PydanticConfig)
class NucleicAcidSequenceMotif(BiologicalEntity):
    """
    A linear nucleotide sequence pattern that is widespread and has, or is conjectured to have, a biological
    significance. e.g. the TATA box promoter motif, transcription factor binding consensus sequences.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:NucleicAcidSequenceMotif"}


@dataclass(config=PydanticConfig)
class RNAProduct(Transcript, GeneProductMixin):

    # Class Variables
    category: ClassVar[str] = {"biolink:RNAProduct"}
    _id_prefixes: ClassVar[List[str]] = ["RNACENTRAL"]


@dataclass(config=PydanticConfig)
class RNAProductIsoform(RNAProduct, GeneProductIsoformMixin):
    """
    Represents a protein that is a specific isoform of the canonical or reference RNA
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:RNAProductIsoform"}
    _id_prefixes: ClassVar[List[str]] = ["RNACENTRAL"]


@dataclass(config=PydanticConfig)
class NoncodingRNAProduct(RNAProduct):

    # Class Variables
    category: ClassVar[str] = {"biolink:NoncodingRNAProduct"}
    _id_prefixes: ClassVar[List[str]] = ["RNACENTRAL", "NCBIGene", "ENSEMBL"]


@dataclass(config=PydanticConfig)
class MicroRNA(NoncodingRNAProduct):

    # Class Variables
    category: ClassVar[str] = {"biolink:MicroRNA"}
    _id_prefixes: ClassVar[List[str]] = ["MIR", "HGNC", "WormBase"]


@dataclass(config=PydanticConfig)
class SiRNA(NoncodingRNAProduct):
    """
    A small RNA molecule that is the product of a longer exogenous or endogenous dsRNA, which is either a bimolecular
    duplex or very long hairpin, processed (via the Dicer pathway) such that numerous siRNAs accumulate from both
    strands of the dsRNA. SRNAs trigger the cleavage of their target molecules.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:SiRNA"}
    _id_prefixes: ClassVar[List[str]] = ["MIR", "HGNC", "WormBase"]


@dataclass(config=PydanticConfig)
class GeneGroupingMixin:
    """
    any grouping of multiple genes or gene products
    """

    has_gene_or_gene_product: Optional[
        Union[List[Union[URIorCURIE, Gene]], Union[URIorCURIE, Gene]]
    ] = field(default_factory=list)

    # Validators

    @validator('has_gene_or_gene_product', allow_reuse=True)
    def convert_has_gene_or_gene_product_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(Gene, value)


@dataclass(config=PydanticConfig)
class ProteinDomain(BiologicalEntity, GeneGroupingMixin, ChemicalEntityOrGeneOrGeneProduct):
    """
    A conserved part of protein sequence and (tertiary) structure that can evolve, function, and exist independently
    of the rest of the protein chain. Protein domains maintain their structure and function independently of the
    proteins in which they are found. e.g. an SH3 domain.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ProteinDomain"}


@dataclass(config=PydanticConfig)
class ProteinFamily(BiologicalEntity, GeneGroupingMixin, ChemicalEntityOrGeneOrGeneProduct):

    # Class Variables
    category: ClassVar[str] = {"biolink:ProteinFamily"}


@dataclass(config=PydanticConfig)
class GeneFamily(BiologicalEntity, GeneGroupingMixin, ChemicalEntityOrGeneOrGeneProduct):
    """
    any grouping of multiple genes or gene products related by common descent
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GeneFamily"}
    _id_prefixes: ClassVar[List[str]] = [
        "PANTHER.FAMILY",
        "HGNC.FAMILY",
        "FB",
        "interpro",
        "CATH",
        "CDD",
        "HAMAP",
        "PFAM",
        "PIRSF",
        "PRINTS",
        "PRODOM",
        "PROSITE",
        "SMART",
        "SUPFAM",
        "TIGRFAM",
        "CATH.SUPERFAMILY",
        "RFAM",
        "KEGG.ORTHOLOGY",
        "EGGNOG",
        "COG",
    ]


@dataclass(config=PydanticConfig)
class Zygosity(Attribute):

    # Class Variables
    category: ClassVar[str] = {"biolink:Zygosity"}


@dataclass(config=PydanticConfig)
class Genotype(BiologicalEntity, PhysicalEssence, GenomicEntity, OntologyClass):
    """
    An information content entity that describes a genome by specifying the total variation in genomic sequence and/or
    gene expression, relative to some established background
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Genotype"}
    _id_prefixes: ClassVar[List[str]] = ["ZFIN", "FB"]

    has_zygosity: Optional[Union[str, Zygosity]] = None


@dataclass(config=PydanticConfig)
class Haplotype(BiologicalEntity, GenomicEntity, PhysicalEssence, OntologyClass):
    """
    A set of zero or more Alleles on a single instance of a Sequence[VMC]
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Haplotype"}


@dataclass(config=PydanticConfig)
class SequenceVariant(BiologicalEntity, GenomicEntity, PhysicalEssence, OntologyClass):
    """
    An allele that varies in its sequence from what is considered the reference allele at that locus.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:SequenceVariant"}
    _id_prefixes: ClassVar[List[str]] = [
        "CAID",
        "CLINVAR",
        "ClinVarVariant",
        "WIKIDATA",
        "DBSNP",
        "MGI",
        "ZFIN",
        "FB",
        "WB",
        "WormBase",
    ]

    id: Union[URIorCURIE, SequenceVariant] = None
    has_gene: Optional[Union[List[Union[URIorCURIE, Gene]], Union[URIorCURIE, Gene]]] = field(
        default_factory=list
    )
    has_biological_sequence: Optional[Union[str, BiologicalSequence]] = None

    # Validators

    @validator('has_gene', allow_reuse=True)
    def convert_has_gene_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(Gene, value)

    @validator('id', allow_reuse=True)
    def validate_required_id(cls, value):
        check_value_is_not_none("id", value)
        check_curie_prefix(SequenceVariant, value)
        return value


@dataclass(config=PydanticConfig)
class Snv(SequenceVariant):
    """
    SNVs are single nucleotide positions in genomic DNA at which different sequence alternatives exist
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Snv"}


@dataclass(config=PydanticConfig)
class ReagentTargetedGene(BiologicalEntity, GenomicEntity, PhysicalEssence, OntologyClass):
    """
    A gene altered in its expression level in the context of some experiment as a result of being targeted by
    gene-knockdown reagent(s) such as a morpholino or RNAi.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ReagentTargetedGene"}


@dataclass(config=PydanticConfig)
class ClinicalAttribute(Attribute):
    """
    Attributes relating to a clinical manifestation
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ClinicalAttribute"}


@dataclass(config=PydanticConfig)
class ClinicalMeasurement(ClinicalAttribute):
    """
    A clinical measurement is a special kind of attribute which results from a laboratory observation from a subject
    individual or sample. Measurements can be connected to their subject by the 'has attribute' slot.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ClinicalMeasurement"}

    has_attribute_type: Union[str, OntologyClass] = None

    # Validators

    @validator('has_attribute_type', allow_reuse=True)
    def validate_required_has_attribute_type(cls, value):
        check_value_is_not_none("has_attribute_type", value)
        return value


@dataclass(config=PydanticConfig)
class ClinicalModifier(ClinicalAttribute):
    """
    Used to characterize and specify the phenotypic abnormalities defined in the phenotypic abnormality sub-ontology,
    with respect to severity, laterality, and other aspects
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ClinicalModifier"}


@dataclass(config=PydanticConfig)
class ClinicalCourse(ClinicalAttribute):
    """
    The course a disease typically takes from its onset, progression in time, and eventual resolution or death of the
    affected individual
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ClinicalCourse"}


@dataclass(config=PydanticConfig)
class Onset(ClinicalCourse):
    """
    The age group in which (disease) symptom manifestations appear
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Onset"}


@dataclass(config=PydanticConfig)
class ClinicalEntity(NamedThing):
    """
    Any entity or process that exists in the clinical domain and outside the biological realm. Diseases are placed
    under biological entities
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ClinicalEntity"}


@dataclass(config=PydanticConfig)
class ClinicalTrial(ClinicalEntity):

    # Class Variables
    category: ClassVar[str] = {"biolink:ClinicalTrial"}


@dataclass(config=PydanticConfig)
class ClinicalIntervention(ClinicalEntity):

    # Class Variables
    category: ClassVar[str] = {"biolink:ClinicalIntervention"}


@dataclass(config=PydanticConfig)
class ClinicalFinding(PhenotypicFeature):
    """
    this category is currently considered broad enough to tag clinical lab measurements and other biological
    attributes taken as 'clinical traits' with some statistical score, for example, a p value in genetic associations.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ClinicalFinding"}
    _id_prefixes: ClassVar[List[str]] = ["LOINC", "NCIT", "EFO"]

    has_attribute: Optional[
        Union[List[Union[str, ClinicalAttribute]], Union[str, ClinicalAttribute]]
    ] = field(default_factory=list)

    # Validators

    @validator('has_attribute', allow_reuse=True)
    def convert_has_attribute_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)


@dataclass(config=PydanticConfig)
class Hospitalization(ClinicalIntervention):

    # Class Variables
    category: ClassVar[str] = {"biolink:Hospitalization"}


@dataclass(config=PydanticConfig)
class SocioeconomicAttribute(Attribute):
    """
    Attributes relating to a socioeconomic manifestation
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:SocioeconomicAttribute"}


@dataclass(config=PydanticConfig)
class Case(IndividualOrganism):
    """
    An individual (human) organism that has a patient role in some clinical context.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Case"}


@dataclass(config=PydanticConfig)
class Cohort(StudyPopulation):
    """
    A group of people banded together or treated as a group who share common characteristics. A cohort 'study' is a
    particular form of longitudinal study that samples a cohort, performing a cross-section at intervals through time.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Cohort"}


@dataclass(config=PydanticConfig)
class ExposureEvent:
    """
    A (possibly time bounded) incidence of a feature of the environment of an organism that influences one or more
    phenotypic features of that organism, potentially mediated by genes
    """

    timepoint: Optional[Union[str, TimeType]] = None


@dataclass(config=PydanticConfig)
class GenomicBackgroundExposure(
    ExposureEvent, GeneGroupingMixin, PhysicalEssence, GenomicEntity, OntologyClass
):
    """
    A genomic background exposure is where an individual's specific genomic background of genes, sequence variants or
    other pre-existing genomic conditions constitute a kind of 'exposure' to the organism, leading to or influencing
    an outcome.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GenomicBackgroundExposure"}


@dataclass(config=PydanticConfig)
class PathologicalEntityMixin:
    """
    A pathological (abnormal) structure or process.
    """


@dataclass(config=PydanticConfig)
class PathologicalProcess(BiologicalProcess, PathologicalEntityMixin):
    """
    A biologic function or a process having an abnormal or deleterious effect at the subcellular, cellular,
    multicellular, or organismal level.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PathologicalProcess"}


@dataclass(config=PydanticConfig)
class PathologicalProcessExposure(ExposureEvent):
    """
    A pathological process, when viewed as an exposure, representing a precondition, leading to or influencing an
    outcome, e.g. autoimmunity leading to disease.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PathologicalProcessExposure"}


@dataclass(config=PydanticConfig)
class PathologicalAnatomicalStructure(AnatomicalEntity, PathologicalEntityMixin):
    """
    An anatomical structure with the potential of have an abnormal or deleterious effect at the subcellular, cellular,
    multicellular, or organismal level.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PathologicalAnatomicalStructure"}


@dataclass(config=PydanticConfig)
class PathologicalAnatomicalExposure(ExposureEvent):
    """
    An abnormal anatomical structure, when viewed as an exposure, representing an precondition, leading to or
    influencing an outcome, e.g. thrombosis leading to an ischemic disease outcome.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PathologicalAnatomicalExposure"}


@dataclass(config=PydanticConfig)
class DiseaseOrPhenotypicFeatureExposure(ExposureEvent, PathologicalEntityMixin):
    """
    A disease or phenotypic feature state, when viewed as an exposure, represents an precondition, leading to or
    influencing an outcome, e.g. HIV predisposing an individual to infections; a relative deficiency of skin
    pigmentation predisposing an individual to skin cancer.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:DiseaseOrPhenotypicFeatureExposure"}


@dataclass(config=PydanticConfig)
class ChemicalExposure(ExposureEvent):
    """
    A chemical exposure is an intake of a particular chemical entity.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ChemicalExposure"}

    has_quantitative_value: Optional[
        Union[List[Union[str, QuantityValue]], Union[str, QuantityValue]]
    ] = field(default_factory=list)

    # Validators

    @validator('has_quantitative_value', allow_reuse=True)
    def convert_has_quantitative_value_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)


@dataclass(config=PydanticConfig)
class ComplexChemicalExposure:
    """
    A complex chemical exposure is an intake of a chemical mixture (e.g. gasoline), other than a drug.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ComplexChemicalExposure"}


@dataclass(config=PydanticConfig)
class DrugExposure(ChemicalExposure, ExposureEvent):
    """
    A drug exposure is an intake of a particular drug.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:DrugExposure"}


@dataclass(config=PydanticConfig)
class DrugToGeneInteractionExposure(DrugExposure, GeneGroupingMixin):
    """
    drug to gene interaction exposure is a drug exposure is where the interactions of the drug with specific genes are
    known to constitute an 'exposure' to the organism, leading to or influencing an outcome.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:DrugToGeneInteractionExposure"}


@dataclass(config=PydanticConfig)
class Treatment(NamedThing, ExposureEvent, ChemicalOrDrugOrTreatment):
    """
    A treatment is targeted at a disease or phenotype and may involve multiple drug 'exposures', medical devices
    and/or procedures
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Treatment"}

    has_drug: Optional[Union[List[Union[URIorCURIE, Drug]], Union[URIorCURIE, Drug]]] = field(
        default_factory=list
    )
    has_device: Optional[Union[List[Union[URIorCURIE, Device]], Union[URIorCURIE, Device]]] = field(
        default_factory=list
    )
    has_procedure: Optional[
        Union[List[Union[URIorCURIE, Procedure]], Union[URIorCURIE, Procedure]]
    ] = field(default_factory=list)

    # Validators

    @validator('has_drug', allow_reuse=True)
    def convert_has_drug_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(Drug, value)

    @validator('has_device', allow_reuse=True)
    def convert_has_device_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(Device, value)

    @validator('has_procedure', allow_reuse=True)
    def convert_has_procedure_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(Procedure, value)


@dataclass(config=PydanticConfig)
class BioticExposure(ExposureEvent):
    """
    An external biotic exposure is an intake of (sometimes pathological) biological organisms (including viruses).
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:BioticExposure"}


@dataclass(config=PydanticConfig)
class EnvironmentalExposure(ExposureEvent):
    """
    A environmental exposure is a factor relating to abiotic processes in the environment including sunlight (UV-B),
    atmospheric (heat, cold, general pollution) and water-born contaminants.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:EnvironmentalExposure"}


@dataclass(config=PydanticConfig)
class GeographicExposure(EnvironmentalExposure, ExposureEvent):
    """
    A geographic exposure is a factor relating to geographic proximity to some impactful entity.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GeographicExposure"}


@dataclass(config=PydanticConfig)
class BehavioralExposure(ExposureEvent):
    """
    A behavioral exposure is a factor relating to behavior impacting an individual.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:BehavioralExposure"}


@dataclass(config=PydanticConfig)
class SocioeconomicExposure(ExposureEvent):
    """
    A socioeconomic exposure is a factor relating to social and financial status of an affected individual (e.g.
    poverty).
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:SocioeconomicExposure"}

    has_attribute: Union[
        List[Union[str, SocioeconomicAttribute]], Union[str, SocioeconomicAttribute]
    ] = None

    # Validators

    @validator('has_attribute', allow_reuse=True)
    def validate_required_has_attribute(cls, value):
        check_value_is_not_none("has_attribute", value)
        convert_scalar_to_list_check_curies(cls, value)
        return value


@dataclass(config=PydanticConfig)
class Outcome:
    """
    An entity that has the role of being the consequence of an exposure event. This is an abstract mixin grouping of
    various categories of possible biological or non-biological (e.g. clinical) outcomes.
    """


@dataclass(config=PydanticConfig)
class PathologicalProcessOutcome(Outcome):
    """
    An outcome resulting from an exposure event which is the manifestation of a pathological process.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PathologicalProcessOutcome"}


@dataclass(config=PydanticConfig)
class PathologicalAnatomicalOutcome(Outcome):
    """
    An outcome resulting from an exposure event which is the manifestation of an abnormal anatomical structure.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PathologicalAnatomicalOutcome"}


@dataclass(config=PydanticConfig)
class DiseaseOrPhenotypicFeatureOutcome(Outcome):
    """
    Physiological outcomes resulting from an exposure event which is the manifestation of a disease or other
    characteristic phenotype.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:DiseaseOrPhenotypicFeatureOutcome"}


@dataclass(config=PydanticConfig)
class BehavioralOutcome(Outcome):
    """
    An outcome resulting from an exposure event which is the manifestation of human behavior.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:BehavioralOutcome"}


@dataclass(config=PydanticConfig)
class HospitalizationOutcome(Outcome):
    """
    An outcome resulting from an exposure event which is the increased manifestation of acute (e.g. emergency room
    visit) or chronic (inpatient) hospitalization.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:HospitalizationOutcome"}


@dataclass(config=PydanticConfig)
class MortalityOutcome(Outcome):
    """
    An outcome of death from resulting from an exposure event.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:MortalityOutcome"}


@dataclass(config=PydanticConfig)
class EpidemiologicalOutcome(Outcome):
    """
    An epidemiological outcome, such as societal disease burden, resulting from an exposure event.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:EpidemiologicalOutcome"}


@dataclass(config=PydanticConfig)
class SocioeconomicOutcome(Outcome):
    """
    An general social or economic outcome, such as healthcare costs, utilization, etc., resulting from an exposure
    event
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:SocioeconomicOutcome"}


@dataclass(config=PydanticConfig)
class Association(Entity):
    """
    A typed association between two entities, supported by evidence
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:Association"}

    subject: Union[URIorCURIE, NamedThing] = None
    predicate: Union[str, PredicateType] = None
    object: Union[URIorCURIE, NamedThing] = None
    relation: Optional[Union[str, str]] = None
    negated: Optional[Union[bool, Bool]] = None
    qualifiers: Optional[Union[List[Union[str, OntologyClass]], Union[str, OntologyClass]]] = field(
        default_factory=list
    )
    publications: Optional[
        Union[List[Union[URIorCURIE, Publication]], Union[URIorCURIE, Publication]]
    ] = field(default_factory=list)
    has_evidence: Optional[
        Union[List[Union[URIorCURIE, EvidenceType]], Union[URIorCURIE, EvidenceType]]
    ] = field(default_factory=list)
    knowledge_source: Optional[
        Union[List[Union[URIorCURIE, InformationResource]], Union[URIorCURIE, InformationResource]]
    ] = field(default_factory=list)
    original_knowledge_source: Optional[Union[URIorCURIE, InformationResource]] = None
    primary_knowledge_source: Optional[Union[URIorCURIE, InformationResource]] = None
    aggregator_knowledge_source: Optional[
        Union[List[Union[URIorCURIE, InformationResource]], Union[URIorCURIE, InformationResource]]
    ] = field(default_factory=list)
    type: Optional[Union[str, str]] = None
    category: Optional[Union[List[Union[str, CategoryType]], Union[str, CategoryType]]] = field(
        default_factory=list
    )

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(NamedThing, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(NamedThing, value)
        return value

    @validator('qualifiers', allow_reuse=True)
    def convert_qualifiers_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    @validator('publications', allow_reuse=True)
    def convert_publications_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(Publication, value)

    @validator('has_evidence', allow_reuse=True)
    def convert_has_evidence_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(EvidenceType, value)

    @validator('knowledge_source', allow_reuse=True)
    def convert_knowledge_source_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(InformationResource, value)

    @validator('original_knowledge_source', allow_reuse=True)
    def check_original_knowledge_source_prefix(cls, value):
        check_curie_prefix(InformationResource, value)
        return value

    @validator('primary_knowledge_source', allow_reuse=True)
    def check_primary_knowledge_source_prefix(cls, value):
        check_curie_prefix(InformationResource, value)
        return value

    @validator('aggregator_knowledge_source', allow_reuse=True)
    def convert_aggregator_knowledge_source_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(InformationResource, value)


@dataclass(config=PydanticConfig)
class ContributorAssociation(Association):
    """
    Any association between an entity (such as a publication) and various agents that contribute to its realisation
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ContributorAssociation"}

    subject: Union[URIorCURIE, InformationContentEntity] = None
    predicate: Union[str, PredicateType] = None
    object: Union[URIorCURIE, Agent] = None
    qualifiers: Optional[Union[List[Union[str, OntologyClass]], Union[str, OntologyClass]]] = field(
        default_factory=list
    )

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(InformationContentEntity, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(Agent, value)
        return value

    @validator('qualifiers', allow_reuse=True)
    def convert_qualifiers_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)


@dataclass(config=PydanticConfig)
class GenotypeToGenotypePartAssociation(Association):
    """
    Any association between one genotype and a genotypic entity that is a sub-component of it
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GenotypeToGenotypePartAssociation"}

    predicate: Union[str, PredicateType] = None
    subject: Union[URIorCURIE, Genotype] = None
    object: Union[URIorCURIE, Genotype] = None

    # Validators

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Genotype, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(Genotype, value)
        return value


@dataclass(config=PydanticConfig)
class GenotypeToGeneAssociation(Association):
    """
    Any association between a genotype and a gene. The genotype have have multiple variants in that gene or a single
    one. There is no assumption of cardinality
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GenotypeToGeneAssociation"}

    predicate: Union[str, PredicateType] = None
    subject: Union[URIorCURIE, Genotype] = None
    object: Union[URIorCURIE, Gene] = None

    # Validators

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Genotype, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(Gene, value)
        return value


@dataclass(config=PydanticConfig)
class GenotypeToVariantAssociation(Association):
    """
    Any association between a genotype and a sequence variant.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GenotypeToVariantAssociation"}

    predicate: Union[str, PredicateType] = None
    subject: Union[URIorCURIE, Genotype] = None
    object: Union[URIorCURIE, SequenceVariant] = None

    # Validators

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Genotype, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(SequenceVariant, value)
        return value


@dataclass(config=PydanticConfig)
class GeneToGeneAssociation(Association):
    """
    abstract parent class for different kinds of gene-gene or gene product to gene product relationships. Includes
    homology and interaction.
    """

    subject: Union[str, GeneOrGeneProduct] = None
    object: Union[str, GeneOrGeneProduct] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        return value


@dataclass(config=PydanticConfig)
class GeneToGeneHomologyAssociation(GeneToGeneAssociation):
    """
    A homology association between two genes. May be orthology (in which case the species of subject and object should
    differ) or paralogy (in which case the species may be the same)
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GeneToGeneHomologyAssociation"}

    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class GeneExpressionMixin:
    """
    Observed gene expression intensity, context (site, stage) and associated phenotypic status within which the
    expression occurs.
    """

    quantifier_qualifier: Optional[Union[str, OntologyClass]] = None
    expression_site: Optional[Union[URIorCURIE, AnatomicalEntity]] = None
    stage_qualifier: Optional[Union[URIorCURIE, LifeStage]] = None
    phenotypic_state: Optional[Union[URIorCURIE, DiseaseOrPhenotypicFeature]] = None

    # Validators

    @validator('expression_site', allow_reuse=True)
    def check_expression_site_prefix(cls, value):
        check_curie_prefix(AnatomicalEntity, value)
        return value

    @validator('stage_qualifier', allow_reuse=True)
    def check_stage_qualifier_prefix(cls, value):
        check_curie_prefix(LifeStage, value)
        return value

    @validator('phenotypic_state', allow_reuse=True)
    def check_phenotypic_state_prefix(cls, value):
        check_curie_prefix(DiseaseOrPhenotypicFeature, value)
        return value


@dataclass(config=PydanticConfig)
class GeneToGeneCoexpressionAssociation(GeneToGeneAssociation, GeneExpressionMixin):
    """
    Indicates that two genes are co-expressed, generally under the same conditions.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GeneToGeneCoexpressionAssociation"}

    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class PairwiseGeneToGeneInteraction(GeneToGeneAssociation):
    """
    An interaction between two genes or two gene products. May be physical (e.g. protein binding) or genetic (between
    genes). May be symmetric (e.g. protein interaction) or directed (e.g. phosphorylation)
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PairwiseGeneToGeneInteraction"}

    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class PairwiseMolecularInteraction(PairwiseGeneToGeneInteraction):
    """
    An interaction at the molecular level between two physical entities
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PairwiseMolecularInteraction"}

    subject: Union[URIorCURIE, MolecularEntity] = None
    id: Union[URIorCURIE, PairwiseMolecularInteraction] = None
    predicate: Union[str, PredicateType] = None
    object: Union[URIorCURIE, MolecularEntity] = None
    interacting_molecules_category: Optional[Union[str, OntologyClass]] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(MolecularEntity, value)
        return value

    @validator('id', allow_reuse=True)
    def validate_required_id(cls, value):
        check_value_is_not_none("id", value)
        check_curie_prefix(PairwiseMolecularInteraction, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(MolecularEntity, value)
        return value


@dataclass(config=PydanticConfig)
class CellLineToEntityAssociationMixin:
    """
    An relationship between a cell line and another entity
    """

    subject: Union[URIorCURIE, CellLine] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(CellLine, value)
        return value


@dataclass(config=PydanticConfig)
class ChemicalEntityToEntityAssociationMixin:
    """
    An interaction between a chemical entity and another entity
    """

    subject: Union[str, ChemicalEntityOrGeneOrGeneProduct] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value


@dataclass(config=PydanticConfig)
class DrugToEntityAssociationMixin(ChemicalEntityToEntityAssociationMixin):
    """
    An interaction between a drug and another entity
    """

    subject: Union[URIorCURIE, Drug] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Drug, value)
        return value


@dataclass(config=PydanticConfig)
class ChemicalToEntityAssociationMixin(ChemicalEntityToEntityAssociationMixin):
    """
    An interaction between a chemical entity and another entity
    """

    subject: Union[str, ChemicalEntityOrGeneOrGeneProduct] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value


@dataclass(config=PydanticConfig)
class CaseToEntityAssociationMixin:
    """
    An abstract association for use where the case is the subject
    """

    subject: Union[URIorCURIE, Case] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Case, value)
        return value


@dataclass(config=PydanticConfig)
class ChemicalToChemicalAssociation(Association, ChemicalToEntityAssociationMixin):
    """
    A relationship between two chemical entities. This can encompass actual interactions as well as temporal causal
    edges, e.g. one chemical converted to another.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ChemicalToChemicalAssociation"}

    object: Union[URIorCURIE, ChemicalEntity] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(ChemicalEntity, value)
        return value


@dataclass(config=PydanticConfig)
class ReactionToParticipantAssociation(ChemicalToChemicalAssociation):

    # Class Variables
    category: ClassVar[str] = {"biolink:ReactionToParticipantAssociation"}

    subject: Union[URIorCURIE, MolecularEntity] = None
    stoichiometry: Optional[Union[int, int]] = None
    reaction_direction: Optional[Union[str, ReactionDirectionEnum]] = None
    reaction_side: Optional[Union[str, ReactionSideEnum]] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(MolecularEntity, value)
        return value


@dataclass(config=PydanticConfig)
class ReactionToCatalystAssociation(ReactionToParticipantAssociation):

    # Class Variables
    category: ClassVar[str] = {"biolink:ReactionToCatalystAssociation"}

    object: Union[str, GeneOrGeneProduct] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        return value


@dataclass(config=PydanticConfig)
class ChemicalToChemicalDerivationAssociation(ChemicalToChemicalAssociation):
    """
    A causal relationship between two chemical entities, where the subject represents the upstream entity and the
    object represents the downstream. For any such association there is an implicit reaction:
    IF
    R has-input C1 AND
    R has-output C2 AND
    R enabled-by P AND
    R type Reaction
    THEN
    C1 derives-into C2 <<catalyst qualifier P>>
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ChemicalToChemicalDerivationAssociation"}

    subject: Union[URIorCURIE, ChemicalEntity] = None
    object: Union[URIorCURIE, ChemicalEntity] = None
    predicate: Union[str, PredicateType] = None
    catalyst_qualifier: Optional[
        Union[List[Union[str, MacromolecularMachineMixin]], Union[str, MacromolecularMachineMixin]]
    ] = field(default_factory=list)

    # Validators

    @validator('catalyst_qualifier', allow_reuse=True)
    def convert_catalyst_qualifier_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(ChemicalEntity, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(ChemicalEntity, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class ChemicalToPathwayAssociation(Association, ChemicalToEntityAssociationMixin):
    """
    An interaction between a chemical entity and a biological process or pathway.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ChemicalToPathwayAssociation"}

    object: Union[URIorCURIE, Pathway] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(Pathway, value)
        return value


@dataclass(config=PydanticConfig)
class ChemicalToGeneAssociation(Association, ChemicalToEntityAssociationMixin):
    """
    An interaction between a chemical entity and a gene or gene product.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ChemicalToGeneAssociation"}

    object: Union[str, GeneOrGeneProduct] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        return value


@dataclass(config=PydanticConfig)
class DrugToGeneAssociation(Association, DrugToEntityAssociationMixin):
    """
    An interaction between a drug and a gene or gene product.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:DrugToGeneAssociation"}

    object: Union[str, GeneOrGeneProduct] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        return value


@dataclass(config=PydanticConfig)
class MaterialSampleToEntityAssociationMixin:
    """
    An association between a material sample and something.
    """

    subject: Union[URIorCURIE, MaterialSample] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(MaterialSample, value)
        return value


@dataclass(config=PydanticConfig)
class MaterialSampleDerivationAssociation(Association):
    """
    An association between a material sample and the material entity from which it is derived.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:MaterialSampleDerivationAssociation"}

    subject: Union[URIorCURIE, MaterialSample] = None
    object: Union[URIorCURIE, NamedThing] = None
    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(MaterialSample, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(NamedThing, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class DiseaseToEntityAssociationMixin:
    subject: Union[URIorCURIE, Disease] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Disease, value)
        return value


@dataclass(config=PydanticConfig)
class EntityToExposureEventAssociationMixin:
    """
    An association between some entity and an exposure event.
    """

    object: Union[str, ExposureEvent] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        return value


@dataclass(config=PydanticConfig)
class DiseaseToExposureEventAssociation(
    Association, DiseaseToEntityAssociationMixin, EntityToExposureEventAssociationMixin
):
    """
    An association between an exposure event and a disease.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:DiseaseToExposureEventAssociation"}


@dataclass(config=PydanticConfig)
class ExposureEventToEntityAssociationMixin:

    # Class Variables
    category: ClassVar[str] = {"biolink:ExposureEventToEntityAssociationMixin"}


@dataclass(config=PydanticConfig)
class EntityToOutcomeAssociationMixin:
    """
    An association between some entity and an outcome
    """

    object: Union[str, Outcome] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        return value


@dataclass(config=PydanticConfig)
class ExposureEventToOutcomeAssociation(
    Association, ExposureEventToEntityAssociationMixin, EntityToOutcomeAssociationMixin
):
    """
    An association between an exposure event and an outcome.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ExposureEventToOutcomeAssociation"}

    has_population_context: Optional[Union[URIorCURIE, PopulationOfIndividualOrganisms]] = None
    has_temporal_context: Optional[Union[str, TimeType]] = None

    # Validators

    @validator('has_population_context', allow_reuse=True)
    def check_has_population_context_prefix(cls, value):
        check_curie_prefix(PopulationOfIndividualOrganisms, value)
        return value


@dataclass(config=PydanticConfig)
class FrequencyQualifierMixin:
    """
    Qualifier for frequency type associations
    """

    frequency_qualifier: Optional[Union[str, FrequencyValue]] = None


@dataclass(config=PydanticConfig)
class EntityToFeatureOrDiseaseQualifiersMixin(FrequencyQualifierMixin):
    """
    Qualifiers for entity to disease or phenotype associations.
    """

    severity_qualifier: Optional[Union[str, SeverityValue]] = None
    onset_qualifier: Optional[Union[str, Onset]] = None


@dataclass(config=PydanticConfig)
class EntityToPhenotypicFeatureAssociationMixin(EntityToFeatureOrDiseaseQualifiersMixin):
    object: Union[URIorCURIE, PhenotypicFeature] = None
    sex_qualifier: Optional[Union[str, BiologicalSex]] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(PhenotypicFeature, value)
        return value


@dataclass(config=PydanticConfig)
class InformationContentEntityToNamedThingAssociation(Association):
    """
    association between a named thing and a information content entity where the specific context of the relationship
    between that named thing and the publication is unknown. For example, model organisms databases often capture the
    knowledge that a gene is found in a journal article, but not specifically the context in which that gene was
    documented in the article. In these cases, this association with the accompanying predicate 'mentions' could be
    used. Conversely, for more specific associations (like 'gene to disease association', the publication should be
    captured as an edge property).
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:InformationContentEntityToNamedThingAssociation"}

    subject: Union[URIorCURIE, NamedThing] = None
    object: Union[URIorCURIE, NamedThing] = None
    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(NamedThing, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(NamedThing, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class EntityToDiseaseAssociationMixin(EntityToFeatureOrDiseaseQualifiersMixin):
    """
    mixin class for any association whose object (target node) is a disease
    """

    object: Union[URIorCURIE, Disease] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(Disease, value)
        return value


@dataclass(config=PydanticConfig)
class DiseaseOrPhenotypicFeatureToEntityAssociationMixin:
    subject: Union[URIorCURIE, DiseaseOrPhenotypicFeature] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(DiseaseOrPhenotypicFeature, value)
        return value


@dataclass(config=PydanticConfig)
class DiseaseOrPhenotypicFeatureToLocationAssociation(
    Association, DiseaseOrPhenotypicFeatureToEntityAssociationMixin
):
    """
    An association between either a disease or a phenotypic feature and an anatomical entity, where the
    disease/feature manifests in that site.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:DiseaseOrPhenotypicFeatureToLocationAssociation"}

    object: Union[URIorCURIE, AnatomicalEntity] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(AnatomicalEntity, value)
        return value


@dataclass(config=PydanticConfig)
class EntityToDiseaseOrPhenotypicFeatureAssociationMixin:
    object: Union[URIorCURIE, DiseaseOrPhenotypicFeature] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(DiseaseOrPhenotypicFeature, value)
        return value


@dataclass(config=PydanticConfig)
class CellLineToDiseaseOrPhenotypicFeatureAssociation(
    Association,
    CellLineToEntityAssociationMixin,
    EntityToDiseaseOrPhenotypicFeatureAssociationMixin,
):
    """
    An relationship between a cell line and a disease or a phenotype, where the cell line is derived from an
    individual with that disease or phenotype.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:CellLineToDiseaseOrPhenotypicFeatureAssociation"}

    subject: Union[URIorCURIE, DiseaseOrPhenotypicFeature] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(DiseaseOrPhenotypicFeature, value)
        return value


@dataclass(config=PydanticConfig)
class ChemicalToDiseaseOrPhenotypicFeatureAssociation(
    Association,
    ChemicalToEntityAssociationMixin,
    EntityToDiseaseOrPhenotypicFeatureAssociationMixin,
):
    """
    An interaction between a chemical entity and a phenotype or disease, where the presence of the chemical gives rise
    to or exacerbates the phenotype.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ChemicalToDiseaseOrPhenotypicFeatureAssociation"}

    object: Union[URIorCURIE, DiseaseOrPhenotypicFeature] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(DiseaseOrPhenotypicFeature, value)
        return value


@dataclass(config=PydanticConfig)
class MaterialSampleToDiseaseOrPhenotypicFeatureAssociation(
    Association,
    MaterialSampleToEntityAssociationMixin,
    EntityToDiseaseOrPhenotypicFeatureAssociationMixin,
):
    """
    An association between a material sample and a disease or phenotype.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:MaterialSampleToDiseaseOrPhenotypicFeatureAssociation"}


@dataclass(config=PydanticConfig)
class GenotypeToEntityAssociationMixin:
    subject: Union[URIorCURIE, Genotype] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Genotype, value)
        return value


@dataclass(config=PydanticConfig)
class GenotypeToPhenotypicFeatureAssociation(
    Association, EntityToPhenotypicFeatureAssociationMixin, GenotypeToEntityAssociationMixin
):
    """
    Any association between one genotype and a phenotypic feature, where having the genotype confers the phenotype,
    either in isolation or through environment
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GenotypeToPhenotypicFeatureAssociation"}

    predicate: Union[str, PredicateType] = None
    subject: Union[URIorCURIE, Genotype] = None

    # Validators

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Genotype, value)
        return value


@dataclass(config=PydanticConfig)
class ExposureEventToPhenotypicFeatureAssociation(
    Association, EntityToPhenotypicFeatureAssociationMixin
):
    """
    Any association between an environment and a phenotypic feature, where being in the environment influences the
    phenotype.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ExposureEventToPhenotypicFeatureAssociation"}

    subject: Union[str, ExposureEvent] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value


@dataclass(config=PydanticConfig)
class DiseaseToPhenotypicFeatureAssociation(
    Association, EntityToPhenotypicFeatureAssociationMixin, DiseaseToEntityAssociationMixin
):
    """
    An association between a disease and a phenotypic feature in which the phenotypic feature is associated with the
    disease in some way.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:DiseaseToPhenotypicFeatureAssociation"}


@dataclass(config=PydanticConfig)
class CaseToPhenotypicFeatureAssociation(
    Association, EntityToPhenotypicFeatureAssociationMixin, CaseToEntityAssociationMixin
):
    """
    An association between a case (e.g. individual patient) and a phenotypic feature in which the individual has or
    has had the phenotype.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:CaseToPhenotypicFeatureAssociation"}


@dataclass(config=PydanticConfig)
class BehaviorToBehavioralFeatureAssociation(
    Association, EntityToPhenotypicFeatureAssociationMixin
):
    """
    An association between an mixture behavior and a behavioral feature manifested by the individual exhibited or has
    exhibited the behavior.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:BehaviorToBehavioralFeatureAssociation"}

    subject: Union[URIorCURIE, Behavior] = None
    object: Union[URIorCURIE, BehavioralFeature] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Behavior, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(BehavioralFeature, value)
        return value


@dataclass(config=PydanticConfig)
class GeneToEntityAssociationMixin:
    subject: Union[str, GeneOrGeneProduct] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value


@dataclass(config=PydanticConfig)
class VariantToEntityAssociationMixin:
    subject: Union[URIorCURIE, SequenceVariant] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(SequenceVariant, value)
        return value


@dataclass(config=PydanticConfig)
class GeneToPhenotypicFeatureAssociation(
    Association, EntityToPhenotypicFeatureAssociationMixin, GeneToEntityAssociationMixin
):

    # Class Variables
    category: ClassVar[str] = {"biolink:GeneToPhenotypicFeatureAssociation"}

    subject: Union[str, GeneOrGeneProduct] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value


@dataclass(config=PydanticConfig)
class GeneToDiseaseAssociation(
    Association, EntityToDiseaseAssociationMixin, GeneToEntityAssociationMixin
):

    # Class Variables
    category: ClassVar[str] = {"biolink:GeneToDiseaseAssociation"}

    subject: Union[str, GeneOrGeneProduct] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value


@dataclass(config=PydanticConfig)
class DruggableGeneToDiseaseAssociation(
    GeneToDiseaseAssociation, EntityToDiseaseAssociationMixin, GeneToEntityAssociationMixin
):

    # Class Variables
    category: ClassVar[str] = {"biolink:DruggableGeneToDiseaseAssociation"}

    subject: Union[str, GeneOrGeneProduct] = None
    predicate: Union[str, PredicateType] = None
    has_evidence: Optional[
        Union[List[Union[str, DruggableGeneCategoryEnum]], Union[str, DruggableGeneCategoryEnum]]
    ] = field(default_factory=list)

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value

    @validator('has_evidence', allow_reuse=True)
    def convert_has_evidence_to_list_check_curies(cls, value):
        return convert_scalar_to_list_check_curies(cls, value)


@dataclass(config=PydanticConfig)
class VariantToGeneAssociation(Association, VariantToEntityAssociationMixin):
    """
    An association between a variant and a gene, where the variant has a genetic association with the gene (i.e. is in
    linkage disequilibrium)
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:VariantToGeneAssociation"}

    object: Union[URIorCURIE, Gene] = None
    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(Gene, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class VariantToGeneExpressionAssociation(VariantToGeneAssociation, GeneExpressionMixin):
    """
    An association between a variant and expression of a gene (i.e. e-QTL)
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:VariantToGeneExpressionAssociation"}

    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class VariantToPopulationAssociation(
    Association, VariantToEntityAssociationMixin, FrequencyQuantifier, FrequencyQualifierMixin
):
    """
    An association between a variant and a population, where the variant has particular frequency in the population
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:VariantToPopulationAssociation"}

    subject: Union[URIorCURIE, SequenceVariant] = None
    object: Union[URIorCURIE, PopulationOfIndividualOrganisms] = None
    has_quotient: Optional[Union[float, float]] = None
    has_count: Optional[Union[int, int]] = None
    has_total: Optional[Union[int, int]] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(SequenceVariant, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(PopulationOfIndividualOrganisms, value)
        return value


@dataclass(config=PydanticConfig)
class PopulationToPopulationAssociation(Association):
    """
    An association between a two populations
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:PopulationToPopulationAssociation"}

    subject: Union[URIorCURIE, PopulationOfIndividualOrganisms] = None
    object: Union[URIorCURIE, PopulationOfIndividualOrganisms] = None
    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(PopulationOfIndividualOrganisms, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(PopulationOfIndividualOrganisms, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class VariantToPhenotypicFeatureAssociation(
    Association, VariantToEntityAssociationMixin, EntityToPhenotypicFeatureAssociationMixin
):

    # Class Variables
    category: ClassVar[str] = {"biolink:VariantToPhenotypicFeatureAssociation"}

    subject: Union[URIorCURIE, SequenceVariant] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(SequenceVariant, value)
        return value


@dataclass(config=PydanticConfig)
class VariantToDiseaseAssociation(
    Association, VariantToEntityAssociationMixin, EntityToDiseaseAssociationMixin
):

    # Class Variables
    category: ClassVar[str] = {"biolink:VariantToDiseaseAssociation"}

    subject: Union[URIorCURIE, NamedThing] = None
    predicate: Union[str, PredicateType] = None
    object: Union[URIorCURIE, NamedThing] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(NamedThing, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(NamedThing, value)
        return value


@dataclass(config=PydanticConfig)
class GenotypeToDiseaseAssociation(
    Association, GenotypeToEntityAssociationMixin, EntityToDiseaseAssociationMixin
):

    # Class Variables
    category: ClassVar[str] = {"biolink:GenotypeToDiseaseAssociation"}

    subject: Union[URIorCURIE, NamedThing] = None
    predicate: Union[str, PredicateType] = None
    object: Union[URIorCURIE, NamedThing] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(NamedThing, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(NamedThing, value)
        return value


@dataclass(config=PydanticConfig)
class ModelToDiseaseAssociationMixin:
    """
    This mixin is used for any association class for which the subject (source node) plays the role of a 'model', in
    that it recapitulates some features of the disease in a way that is useful for studying the disease outside a
    patient carrying the disease
    """

    subject: Union[URIorCURIE, NamedThing] = None
    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(NamedThing, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class GeneAsAModelOfDiseaseAssociation(
    GeneToDiseaseAssociation, ModelToDiseaseAssociationMixin, EntityToDiseaseAssociationMixin
):

    # Class Variables
    category: ClassVar[str] = {"biolink:GeneAsAModelOfDiseaseAssociation"}

    subject: Union[str, GeneOrGeneProduct] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value


@dataclass(config=PydanticConfig)
class VariantAsAModelOfDiseaseAssociation(
    VariantToDiseaseAssociation, ModelToDiseaseAssociationMixin, EntityToDiseaseAssociationMixin
):

    # Class Variables
    category: ClassVar[str] = {"biolink:VariantAsAModelOfDiseaseAssociation"}

    subject: Union[URIorCURIE, SequenceVariant] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(SequenceVariant, value)
        return value


@dataclass(config=PydanticConfig)
class GenotypeAsAModelOfDiseaseAssociation(
    GenotypeToDiseaseAssociation, ModelToDiseaseAssociationMixin, EntityToDiseaseAssociationMixin
):

    # Class Variables
    category: ClassVar[str] = {"biolink:GenotypeAsAModelOfDiseaseAssociation"}

    subject: Union[URIorCURIE, Genotype] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Genotype, value)
        return value


@dataclass(config=PydanticConfig)
class CellLineAsAModelOfDiseaseAssociation(
    CellLineToDiseaseOrPhenotypicFeatureAssociation,
    ModelToDiseaseAssociationMixin,
    EntityToDiseaseAssociationMixin,
):

    # Class Variables
    category: ClassVar[str] = {"biolink:CellLineAsAModelOfDiseaseAssociation"}

    subject: Union[URIorCURIE, CellLine] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(CellLine, value)
        return value


@dataclass(config=PydanticConfig)
class OrganismalEntityAsAModelOfDiseaseAssociation(
    Association, ModelToDiseaseAssociationMixin, EntityToDiseaseAssociationMixin
):

    # Class Variables
    category: ClassVar[str] = {"biolink:OrganismalEntityAsAModelOfDiseaseAssociation"}

    subject: Union[URIorCURIE, OrganismalEntity] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(OrganismalEntity, value)
        return value


@dataclass(config=PydanticConfig)
class OrganismToOrganismAssociation(Association):

    # Class Variables
    category: ClassVar[str] = {"biolink:OrganismToOrganismAssociation"}

    subject: Union[URIorCURIE, IndividualOrganism] = None
    object: Union[URIorCURIE, IndividualOrganism] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(IndividualOrganism, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(IndividualOrganism, value)
        return value


@dataclass(config=PydanticConfig)
class TaxonToTaxonAssociation(Association):

    # Class Variables
    category: ClassVar[str] = {"biolink:TaxonToTaxonAssociation"}

    subject: Union[URIorCURIE, OrganismTaxon] = None
    object: Union[URIorCURIE, OrganismTaxon] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(OrganismTaxon, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(OrganismTaxon, value)
        return value


@dataclass(config=PydanticConfig)
class GeneHasVariantThatContributesToDiseaseAssociation(GeneToDiseaseAssociation):

    # Class Variables
    category: ClassVar[str] = {"biolink:GeneHasVariantThatContributesToDiseaseAssociation"}

    subject: Union[str, GeneOrGeneProduct] = None
    sequence_variant_qualifier: Optional[Union[URIorCURIE, SequenceVariant]] = None

    # Validators

    @validator('sequence_variant_qualifier', allow_reuse=True)
    def check_sequence_variant_qualifier_prefix(cls, value):
        check_curie_prefix(SequenceVariant, value)
        return value

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value


@dataclass(config=PydanticConfig)
class GeneToExpressionSiteAssociation(Association):
    """
    An association between a gene and a gene expression site, possibly qualified by stage/timing info.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GeneToExpressionSiteAssociation"}

    subject: Union[str, GeneOrGeneProduct] = None
    object: Union[URIorCURIE, AnatomicalEntity] = None
    predicate: Union[str, PredicateType] = None
    stage_qualifier: Optional[Union[URIorCURIE, LifeStage]] = None
    quantifier_qualifier: Optional[Union[str, OntologyClass]] = None

    # Validators

    @validator('stage_qualifier', allow_reuse=True)
    def check_stage_qualifier_prefix(cls, value):
        check_curie_prefix(LifeStage, value)
        return value

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(AnatomicalEntity, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class SequenceVariantModulatesTreatmentAssociation(Association):
    """
    An association between a sequence variant and a treatment or health intervention. The treatment object itself
    encompasses both the disease and the drug used.
    """

    subject: Union[URIorCURIE, SequenceVariant] = None
    object: Union[URIorCURIE, Treatment] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(SequenceVariant, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(Treatment, value)
        return value


@dataclass(config=PydanticConfig)
class FunctionalAssociation(Association):
    """
    An association between a macromolecular machine mixin (gene, gene product or complex of gene products) and either
    a molecular activity, a biological process or a cellular location in which a function is executed.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:FunctionalAssociation"}

    subject: Union[str, MacromolecularMachineMixin] = None
    object: Union[str, GeneOntologyClass] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        return value


@dataclass(config=PydanticConfig)
class MacromolecularMachineToEntityAssociationMixin:
    """
    an association which has a macromolecular machine mixin as a subject
    """

    subject: Union[URIorCURIE, NamedThing] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(NamedThing, value)
        return value


@dataclass(config=PydanticConfig)
class MacromolecularMachineToMolecularActivityAssociation(
    FunctionalAssociation, MacromolecularMachineToEntityAssociationMixin
):
    """
    A functional association between a macromolecular machine (gene, gene product or complex) and a molecular activity
    (as represented in the GO molecular function branch), where the entity carries out the activity, or contributes to
    its execution.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:MacromolecularMachineToMolecularActivityAssociation"}

    object: Union[URIorCURIE, MolecularActivity] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(MolecularActivity, value)
        return value


@dataclass(config=PydanticConfig)
class MacromolecularMachineToBiologicalProcessAssociation(
    FunctionalAssociation, MacromolecularMachineToEntityAssociationMixin
):
    """
    A functional association between a macromolecular machine (gene, gene product or complex) and a biological process
    or pathway (as represented in the GO biological process branch), where the entity carries out some part of the
    process, regulates it, or acts upstream of it.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:MacromolecularMachineToBiologicalProcessAssociation"}

    object: Union[URIorCURIE, BiologicalProcess] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(BiologicalProcess, value)
        return value


@dataclass(config=PydanticConfig)
class MacromolecularMachineToCellularComponentAssociation(
    FunctionalAssociation, MacromolecularMachineToEntityAssociationMixin
):
    """
    A functional association between a macromolecular machine (gene, gene product or complex) and a cellular component
    (as represented in the GO cellular component branch), where the entity carries out its function in the cellular
    component.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:MacromolecularMachineToCellularComponentAssociation"}

    object: Union[URIorCURIE, CellularComponent] = None

    # Validators

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(CellularComponent, value)
        return value


@dataclass(config=PydanticConfig)
class MolecularActivityToChemicalEntityAssociation(Association):
    """
    Added in response to capturing relationship between microbiome activities as measured via measurements of blood
    analytes as collected via blood and stool samples
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:MolecularActivityToChemicalEntityAssociation"}

    subject: Union[URIorCURIE, MolecularActivity] = None
    object: Union[URIorCURIE, ChemicalEntity] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(MolecularActivity, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(ChemicalEntity, value)
        return value


@dataclass(config=PydanticConfig)
class MolecularActivityToMolecularActivityAssociation(Association):
    """
    Added in response to capturing relationship between microbiome activities as measured via measurements of blood
    analytes as collected via blood and stool samples
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:MolecularActivityToMolecularActivityAssociation"}

    subject: Union[URIorCURIE, MolecularActivity] = None
    object: Union[URIorCURIE, MolecularActivity] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(MolecularActivity, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(MolecularActivity, value)
        return value


@dataclass(config=PydanticConfig)
class GeneToGoTermAssociation(FunctionalAssociation):

    # Class Variables
    category: ClassVar[str] = {"biolink:GeneToGoTermAssociation"}

    subject: Union[URIorCURIE, Gene] = None
    object: Union[str, GeneOntologyClass] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Gene, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        return value


@dataclass(config=PydanticConfig)
class EntityToDiseaseAssociation(Association):

    # Class Variables
    category: ClassVar[str] = {"biolink:EntityToDiseaseAssociation"}

    FDA_approval_status: Optional[Union[str, FDAApprovalStatusEnum]] = None


@dataclass(config=PydanticConfig)
class EntityToPhenotypicFeatureAssociation(Association):

    # Class Variables
    category: ClassVar[str] = {"biolink:EntityToPhenotypicFeatureAssociation"}

    FDA_approval_status: Optional[Union[str, FDAApprovalStatusEnum]] = None


@dataclass(config=PydanticConfig)
class SequenceAssociation(Association):
    """
    An association between a sequence feature and a nucleic acid entity it is localized to.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:SequenceAssociation"}


@dataclass(config=PydanticConfig)
class GenomicSequenceLocalization(SequenceAssociation):
    """
    A relationship between a sequence feature and a nucleic acid entity it is localized to. The reference entity may
    be a chromosome, chromosome region or information entity such as a contig.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GenomicSequenceLocalization"}

    subject: Union[URIorCURIE, NucleicAcidEntity] = None
    object: Union[URIorCURIE, NucleicAcidEntity] = None
    predicate: Union[str, PredicateType] = None
    start_interbase_coordinate: Optional[Union[int, int]] = None
    end_interbase_coordinate: Optional[Union[int, int]] = None
    genome_build: Optional[Union[str, StrandEnum]] = None
    strand: Optional[Union[str, StrandEnum]] = None
    phase: Optional[Union[str, PhaseEnum]] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(NucleicAcidEntity, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(NucleicAcidEntity, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class SequenceFeatureRelationship(Association):
    """
    For example, a particular exon is part of a particular transcript or gene
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:SequenceFeatureRelationship"}

    subject: Union[URIorCURIE, NucleicAcidEntity] = None
    object: Union[URIorCURIE, NucleicAcidEntity] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(NucleicAcidEntity, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(NucleicAcidEntity, value)
        return value


@dataclass(config=PydanticConfig)
class TranscriptToGeneRelationship(SequenceFeatureRelationship):
    """
    A gene is a collection of transcripts
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:TranscriptToGeneRelationship"}

    subject: Union[URIorCURIE, Transcript] = None
    object: Union[URIorCURIE, Gene] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Transcript, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(Gene, value)
        return value


@dataclass(config=PydanticConfig)
class GeneToGeneProductRelationship(SequenceFeatureRelationship):
    """
    A gene is transcribed and potentially translated to a gene product
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GeneToGeneProductRelationship"}

    subject: Union[URIorCURIE, Gene] = None
    object: Union[str, GeneProductMixin] = None
    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Gene, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class ExonToTranscriptRelationship(SequenceFeatureRelationship):
    """
    A transcript is formed from multiple exons
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:ExonToTranscriptRelationship"}

    subject: Union[URIorCURIE, Exon] = None
    object: Union[URIorCURIE, Transcript] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(Exon, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(Transcript, value)
        return value


@dataclass(config=PydanticConfig)
class GeneRegulatoryRelationship(Association):
    """
    A regulatory relationship between two genes
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:GeneRegulatoryRelationship"}

    predicate: Union[str, PredicateType] = None
    subject: Union[str, GeneOrGeneProduct] = None
    object: Union[str, GeneOrGeneProduct] = None

    # Validators

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        return value


@dataclass(config=PydanticConfig)
class AnatomicalEntityToAnatomicalEntityAssociation(Association):
    subject: Union[URIorCURIE, AnatomicalEntity] = None
    object: Union[URIorCURIE, AnatomicalEntity] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(AnatomicalEntity, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(AnatomicalEntity, value)
        return value


@dataclass(config=PydanticConfig)
class AnatomicalEntityToAnatomicalEntityPartOfAssociation(
    AnatomicalEntityToAnatomicalEntityAssociation
):
    """
    A relationship between two anatomical entities where the relationship is mereological, i.e the two entities are
    related by parthood. This includes relationships between cellular components and cells, between cells and tissues,
    tissues and whole organisms
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:AnatomicalEntityToAnatomicalEntityPartOfAssociation"}

    subject: Union[URIorCURIE, AnatomicalEntity] = None
    object: Union[URIorCURIE, AnatomicalEntity] = None
    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(AnatomicalEntity, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(AnatomicalEntity, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class AnatomicalEntityToAnatomicalEntityOntogenicAssociation(
    AnatomicalEntityToAnatomicalEntityAssociation
):
    """
    A relationship between two anatomical entities where the relationship is ontogenic, i.e. the two entities are
    related by development. A number of different relationship types can be used to specify the precise nature of the
    relationship.
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:AnatomicalEntityToAnatomicalEntityOntogenicAssociation"}

    subject: Union[URIorCURIE, AnatomicalEntity] = None
    object: Union[URIorCURIE, AnatomicalEntity] = None
    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(AnatomicalEntity, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(AnatomicalEntity, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class OrganismTaxonToEntityAssociation:
    """
    An association between an organism taxon and another entity
    """

    subject: Union[URIorCURIE, OrganismTaxon] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(OrganismTaxon, value)
        return value


@dataclass(config=PydanticConfig)
class OrganismTaxonToOrganismTaxonAssociation(Association, OrganismTaxonToEntityAssociation):
    """
    A relationship between two organism taxon nodes
    """

    subject: Union[URIorCURIE, OrganismTaxon] = None
    object: Union[URIorCURIE, OrganismTaxon] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(OrganismTaxon, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(OrganismTaxon, value)
        return value


@dataclass(config=PydanticConfig)
class OrganismTaxonToOrganismTaxonSpecialization(OrganismTaxonToOrganismTaxonAssociation):
    """
    A child-parent relationship between two taxa. For example: Homo sapiens subclass_of Homo
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:OrganismTaxonToOrganismTaxonSpecialization"}

    subject: Union[URIorCURIE, OrganismTaxon] = None
    object: Union[URIorCURIE, OrganismTaxon] = None
    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(OrganismTaxon, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(OrganismTaxon, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class OrganismTaxonToOrganismTaxonInteraction(OrganismTaxonToOrganismTaxonAssociation):
    """
    An interaction relationship between two taxa. This may be a symbiotic relationship (encompassing mutualism and
    parasitism), or it may be non-symbiotic. Example: plague transmitted_by flea; cattle domesticated_by Homo sapiens;
    plague infects Homo sapiens
    """

    # Class Variables
    category: ClassVar[str] = {"biolink:OrganismTaxonToOrganismTaxonInteraction"}

    subject: Union[URIorCURIE, OrganismTaxon] = None
    object: Union[URIorCURIE, OrganismTaxon] = None
    predicate: Union[str, PredicateType] = None
    associated_environmental_context: Optional[Union[str, str]] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(OrganismTaxon, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(OrganismTaxon, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


@dataclass(config=PydanticConfig)
class OrganismTaxonToEnvironmentAssociation(Association, OrganismTaxonToEntityAssociation):
    subject: Union[URIorCURIE, OrganismTaxon] = None
    object: Union[URIorCURIE, NamedThing] = None
    predicate: Union[str, PredicateType] = None

    # Validators

    @validator('subject', allow_reuse=True)
    def validate_required_subject(cls, value):
        check_value_is_not_none("subject", value)
        check_curie_prefix(OrganismTaxon, value)
        return value

    @validator('object', allow_reuse=True)
    def validate_required_object(cls, value):
        check_value_is_not_none("object", value)
        check_curie_prefix(NamedThing, value)
        return value

    @validator('predicate', allow_reuse=True)
    def validate_required_predicate(cls, value):
        check_value_is_not_none("predicate", value)
        return value


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
OntologyClass.__pydantic_model__.update_forward_refs()
Annotation.__pydantic_model__.update_forward_refs()
QuantityValue.__pydantic_model__.update_forward_refs()
Attribute.__pydantic_model__.update_forward_refs()
ChemicalRole.__pydantic_model__.update_forward_refs()
BiologicalSex.__pydantic_model__.update_forward_refs()
PhenotypicSex.__pydantic_model__.update_forward_refs()
GenotypicSex.__pydantic_model__.update_forward_refs()
SeverityValue.__pydantic_model__.update_forward_refs()
RelationshipQuantifier.__pydantic_model__.update_forward_refs()
SensitivityQuantifier.__pydantic_model__.update_forward_refs()
SpecificityQuantifier.__pydantic_model__.update_forward_refs()
PathognomonicityQuantifier.__pydantic_model__.update_forward_refs()
FrequencyQuantifier.__pydantic_model__.update_forward_refs()
ChemicalOrDrugOrTreatment.__pydantic_model__.update_forward_refs()
Entity.__pydantic_model__.update_forward_refs()
NamedThing.__pydantic_model__.update_forward_refs()
RelationshipType.__pydantic_model__.update_forward_refs()
GeneOntologyClass.__pydantic_model__.update_forward_refs()
UnclassifiedOntologyClass.__pydantic_model__.update_forward_refs()
TaxonomicRank.__pydantic_model__.update_forward_refs()
OrganismTaxon.__pydantic_model__.update_forward_refs()
Event.__pydantic_model__.update_forward_refs()
AdministrativeEntity.__pydantic_model__.update_forward_refs()
Agent.__pydantic_model__.update_forward_refs()
InformationContentEntity.__pydantic_model__.update_forward_refs()
Dataset.__pydantic_model__.update_forward_refs()
DatasetDistribution.__pydantic_model__.update_forward_refs()
DatasetVersion.__pydantic_model__.update_forward_refs()
DatasetSummary.__pydantic_model__.update_forward_refs()
ConfidenceLevel.__pydantic_model__.update_forward_refs()
EvidenceType.__pydantic_model__.update_forward_refs()
InformationResource.__pydantic_model__.update_forward_refs()
Publication.__pydantic_model__.update_forward_refs()
Book.__pydantic_model__.update_forward_refs()
BookChapter.__pydantic_model__.update_forward_refs()
Serial.__pydantic_model__.update_forward_refs()
Article.__pydantic_model__.update_forward_refs()
PhysicalEssenceOrOccurrent.__pydantic_model__.update_forward_refs()
PhysicalEssence.__pydantic_model__.update_forward_refs()
PhysicalEntity.__pydantic_model__.update_forward_refs()
Occurrent.__pydantic_model__.update_forward_refs()
ActivityAndBehavior.__pydantic_model__.update_forward_refs()
Activity.__pydantic_model__.update_forward_refs()
Procedure.__pydantic_model__.update_forward_refs()
Phenomenon.__pydantic_model__.update_forward_refs()
Device.__pydantic_model__.update_forward_refs()
SubjectOfInvestigation.__pydantic_model__.update_forward_refs()
MaterialSample.__pydantic_model__.update_forward_refs()
PlanetaryEntity.__pydantic_model__.update_forward_refs()
EnvironmentalProcess.__pydantic_model__.update_forward_refs()
EnvironmentalFeature.__pydantic_model__.update_forward_refs()
GeographicLocation.__pydantic_model__.update_forward_refs()
GeographicLocationAtTime.__pydantic_model__.update_forward_refs()
BiologicalEntity.__pydantic_model__.update_forward_refs()
ThingWithTaxon.__pydantic_model__.update_forward_refs()
GenomicEntity.__pydantic_model__.update_forward_refs()
ChemicalSubstance.__pydantic_model__.update_forward_refs()
BiologicalProcessOrActivity.__pydantic_model__.update_forward_refs()
MolecularActivity.__pydantic_model__.update_forward_refs()
BiologicalProcess.__pydantic_model__.update_forward_refs()
Pathway.__pydantic_model__.update_forward_refs()
PhysiologicalProcess.__pydantic_model__.update_forward_refs()
Behavior.__pydantic_model__.update_forward_refs()
OrganismAttribute.__pydantic_model__.update_forward_refs()
PhenotypicQuality.__pydantic_model__.update_forward_refs()
Inheritance.__pydantic_model__.update_forward_refs()
OrganismalEntity.__pydantic_model__.update_forward_refs()
LifeStage.__pydantic_model__.update_forward_refs()
IndividualOrganism.__pydantic_model__.update_forward_refs()
PopulationOfIndividualOrganisms.__pydantic_model__.update_forward_refs()
StudyPopulation.__pydantic_model__.update_forward_refs()
DiseaseOrPhenotypicFeature.__pydantic_model__.update_forward_refs()
Disease.__pydantic_model__.update_forward_refs()
PhenotypicFeature.__pydantic_model__.update_forward_refs()
BehavioralFeature.__pydantic_model__.update_forward_refs()
AnatomicalEntity.__pydantic_model__.update_forward_refs()
CellularComponent.__pydantic_model__.update_forward_refs()
Cell.__pydantic_model__.update_forward_refs()
CellLine.__pydantic_model__.update_forward_refs()
GrossAnatomicalStructure.__pydantic_model__.update_forward_refs()
ChemicalEntityOrGeneOrGeneProduct.__pydantic_model__.update_forward_refs()
ChemicalEntityOrProteinOrPolypeptide.__pydantic_model__.update_forward_refs()
ChemicalEntity.__pydantic_model__.update_forward_refs()
MolecularEntity.__pydantic_model__.update_forward_refs()
SmallMolecule.__pydantic_model__.update_forward_refs()
ChemicalMixture.__pydantic_model__.update_forward_refs()
NucleicAcidEntity.__pydantic_model__.update_forward_refs()
MolecularMixture.__pydantic_model__.update_forward_refs()
ComplexMolecularMixture.__pydantic_model__.update_forward_refs()
ProcessedMaterial.__pydantic_model__.update_forward_refs()
Drug.__pydantic_model__.update_forward_refs()
EnvironmentalFoodContaminant.__pydantic_model__.update_forward_refs()
FoodAdditive.__pydantic_model__.update_forward_refs()
Nutrient.__pydantic_model__.update_forward_refs()
Macronutrient.__pydantic_model__.update_forward_refs()
Micronutrient.__pydantic_model__.update_forward_refs()
Vitamin.__pydantic_model__.update_forward_refs()
Food.__pydantic_model__.update_forward_refs()
MacromolecularMachineMixin.__pydantic_model__.update_forward_refs()
GeneOrGeneProduct.__pydantic_model__.update_forward_refs()
Gene.__pydantic_model__.update_forward_refs()
GeneProductMixin.__pydantic_model__.update_forward_refs()
GeneProductIsoformMixin.__pydantic_model__.update_forward_refs()
MacromolecularComplexMixin.__pydantic_model__.update_forward_refs()
Genome.__pydantic_model__.update_forward_refs()
Exon.__pydantic_model__.update_forward_refs()
Transcript.__pydantic_model__.update_forward_refs()
CodingSequence.__pydantic_model__.update_forward_refs()
Polypeptide.__pydantic_model__.update_forward_refs()
Protein.__pydantic_model__.update_forward_refs()
ProteinIsoform.__pydantic_model__.update_forward_refs()
NucleicAcidSequenceMotif.__pydantic_model__.update_forward_refs()
RNAProduct.__pydantic_model__.update_forward_refs()
RNAProductIsoform.__pydantic_model__.update_forward_refs()
NoncodingRNAProduct.__pydantic_model__.update_forward_refs()
MicroRNA.__pydantic_model__.update_forward_refs()
SiRNA.__pydantic_model__.update_forward_refs()
GeneGroupingMixin.__pydantic_model__.update_forward_refs()
ProteinDomain.__pydantic_model__.update_forward_refs()
ProteinFamily.__pydantic_model__.update_forward_refs()
GeneFamily.__pydantic_model__.update_forward_refs()
Zygosity.__pydantic_model__.update_forward_refs()
Genotype.__pydantic_model__.update_forward_refs()
Haplotype.__pydantic_model__.update_forward_refs()
SequenceVariant.__pydantic_model__.update_forward_refs()
Snv.__pydantic_model__.update_forward_refs()
ReagentTargetedGene.__pydantic_model__.update_forward_refs()
ClinicalAttribute.__pydantic_model__.update_forward_refs()
ClinicalMeasurement.__pydantic_model__.update_forward_refs()
ClinicalModifier.__pydantic_model__.update_forward_refs()
ClinicalCourse.__pydantic_model__.update_forward_refs()
Onset.__pydantic_model__.update_forward_refs()
ClinicalEntity.__pydantic_model__.update_forward_refs()
ClinicalTrial.__pydantic_model__.update_forward_refs()
ClinicalIntervention.__pydantic_model__.update_forward_refs()
ClinicalFinding.__pydantic_model__.update_forward_refs()
Hospitalization.__pydantic_model__.update_forward_refs()
SocioeconomicAttribute.__pydantic_model__.update_forward_refs()
Case.__pydantic_model__.update_forward_refs()
Cohort.__pydantic_model__.update_forward_refs()
ExposureEvent.__pydantic_model__.update_forward_refs()
GenomicBackgroundExposure.__pydantic_model__.update_forward_refs()
PathologicalEntityMixin.__pydantic_model__.update_forward_refs()
PathologicalProcess.__pydantic_model__.update_forward_refs()
PathologicalProcessExposure.__pydantic_model__.update_forward_refs()
PathologicalAnatomicalStructure.__pydantic_model__.update_forward_refs()
PathologicalAnatomicalExposure.__pydantic_model__.update_forward_refs()
DiseaseOrPhenotypicFeatureExposure.__pydantic_model__.update_forward_refs()
ChemicalExposure.__pydantic_model__.update_forward_refs()
ComplexChemicalExposure.__pydantic_model__.update_forward_refs()
DrugExposure.__pydantic_model__.update_forward_refs()
DrugToGeneInteractionExposure.__pydantic_model__.update_forward_refs()
Treatment.__pydantic_model__.update_forward_refs()
BioticExposure.__pydantic_model__.update_forward_refs()
EnvironmentalExposure.__pydantic_model__.update_forward_refs()
GeographicExposure.__pydantic_model__.update_forward_refs()
BehavioralExposure.__pydantic_model__.update_forward_refs()
SocioeconomicExposure.__pydantic_model__.update_forward_refs()
Outcome.__pydantic_model__.update_forward_refs()
PathologicalProcessOutcome.__pydantic_model__.update_forward_refs()
PathologicalAnatomicalOutcome.__pydantic_model__.update_forward_refs()
DiseaseOrPhenotypicFeatureOutcome.__pydantic_model__.update_forward_refs()
BehavioralOutcome.__pydantic_model__.update_forward_refs()
HospitalizationOutcome.__pydantic_model__.update_forward_refs()
MortalityOutcome.__pydantic_model__.update_forward_refs()
EpidemiologicalOutcome.__pydantic_model__.update_forward_refs()
SocioeconomicOutcome.__pydantic_model__.update_forward_refs()
Association.__pydantic_model__.update_forward_refs()
ContributorAssociation.__pydantic_model__.update_forward_refs()
GenotypeToGenotypePartAssociation.__pydantic_model__.update_forward_refs()
GenotypeToGeneAssociation.__pydantic_model__.update_forward_refs()
GenotypeToVariantAssociation.__pydantic_model__.update_forward_refs()
GeneToGeneAssociation.__pydantic_model__.update_forward_refs()
GeneToGeneHomologyAssociation.__pydantic_model__.update_forward_refs()
GeneExpressionMixin.__pydantic_model__.update_forward_refs()
GeneToGeneCoexpressionAssociation.__pydantic_model__.update_forward_refs()
PairwiseGeneToGeneInteraction.__pydantic_model__.update_forward_refs()
PairwiseMolecularInteraction.__pydantic_model__.update_forward_refs()
CellLineToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
ChemicalEntityToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
DrugToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
ChemicalToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
CaseToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
ChemicalToChemicalAssociation.__pydantic_model__.update_forward_refs()
ReactionToParticipantAssociation.__pydantic_model__.update_forward_refs()
ReactionToCatalystAssociation.__pydantic_model__.update_forward_refs()
ChemicalToChemicalDerivationAssociation.__pydantic_model__.update_forward_refs()
ChemicalToPathwayAssociation.__pydantic_model__.update_forward_refs()
ChemicalToGeneAssociation.__pydantic_model__.update_forward_refs()
DrugToGeneAssociation.__pydantic_model__.update_forward_refs()
MaterialSampleToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
MaterialSampleDerivationAssociation.__pydantic_model__.update_forward_refs()
DiseaseToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
EntityToExposureEventAssociationMixin.__pydantic_model__.update_forward_refs()
DiseaseToExposureEventAssociation.__pydantic_model__.update_forward_refs()
ExposureEventToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
EntityToOutcomeAssociationMixin.__pydantic_model__.update_forward_refs()
ExposureEventToOutcomeAssociation.__pydantic_model__.update_forward_refs()
FrequencyQualifierMixin.__pydantic_model__.update_forward_refs()
EntityToFeatureOrDiseaseQualifiersMixin.__pydantic_model__.update_forward_refs()
EntityToPhenotypicFeatureAssociationMixin.__pydantic_model__.update_forward_refs()
InformationContentEntityToNamedThingAssociation.__pydantic_model__.update_forward_refs()
EntityToDiseaseAssociationMixin.__pydantic_model__.update_forward_refs()
DiseaseOrPhenotypicFeatureToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
DiseaseOrPhenotypicFeatureToLocationAssociation.__pydantic_model__.update_forward_refs()
EntityToDiseaseOrPhenotypicFeatureAssociationMixin.__pydantic_model__.update_forward_refs()
CellLineToDiseaseOrPhenotypicFeatureAssociation.__pydantic_model__.update_forward_refs()
ChemicalToDiseaseOrPhenotypicFeatureAssociation.__pydantic_model__.update_forward_refs()
MaterialSampleToDiseaseOrPhenotypicFeatureAssociation.__pydantic_model__.update_forward_refs()
GenotypeToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
GenotypeToPhenotypicFeatureAssociation.__pydantic_model__.update_forward_refs()
ExposureEventToPhenotypicFeatureAssociation.__pydantic_model__.update_forward_refs()
DiseaseToPhenotypicFeatureAssociation.__pydantic_model__.update_forward_refs()
CaseToPhenotypicFeatureAssociation.__pydantic_model__.update_forward_refs()
BehaviorToBehavioralFeatureAssociation.__pydantic_model__.update_forward_refs()
GeneToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
VariantToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
GeneToPhenotypicFeatureAssociation.__pydantic_model__.update_forward_refs()
GeneToDiseaseAssociation.__pydantic_model__.update_forward_refs()
DruggableGeneToDiseaseAssociation.__pydantic_model__.update_forward_refs()
VariantToGeneAssociation.__pydantic_model__.update_forward_refs()
VariantToGeneExpressionAssociation.__pydantic_model__.update_forward_refs()
VariantToPopulationAssociation.__pydantic_model__.update_forward_refs()
PopulationToPopulationAssociation.__pydantic_model__.update_forward_refs()
VariantToPhenotypicFeatureAssociation.__pydantic_model__.update_forward_refs()
VariantToDiseaseAssociation.__pydantic_model__.update_forward_refs()
GenotypeToDiseaseAssociation.__pydantic_model__.update_forward_refs()
ModelToDiseaseAssociationMixin.__pydantic_model__.update_forward_refs()
GeneAsAModelOfDiseaseAssociation.__pydantic_model__.update_forward_refs()
VariantAsAModelOfDiseaseAssociation.__pydantic_model__.update_forward_refs()
GenotypeAsAModelOfDiseaseAssociation.__pydantic_model__.update_forward_refs()
CellLineAsAModelOfDiseaseAssociation.__pydantic_model__.update_forward_refs()
OrganismalEntityAsAModelOfDiseaseAssociation.__pydantic_model__.update_forward_refs()
OrganismToOrganismAssociation.__pydantic_model__.update_forward_refs()
TaxonToTaxonAssociation.__pydantic_model__.update_forward_refs()
GeneHasVariantThatContributesToDiseaseAssociation.__pydantic_model__.update_forward_refs()
GeneToExpressionSiteAssociation.__pydantic_model__.update_forward_refs()
SequenceVariantModulatesTreatmentAssociation.__pydantic_model__.update_forward_refs()
FunctionalAssociation.__pydantic_model__.update_forward_refs()
MacromolecularMachineToEntityAssociationMixin.__pydantic_model__.update_forward_refs()
MacromolecularMachineToMolecularActivityAssociation.__pydantic_model__.update_forward_refs()
MacromolecularMachineToBiologicalProcessAssociation.__pydantic_model__.update_forward_refs()
MacromolecularMachineToCellularComponentAssociation.__pydantic_model__.update_forward_refs()
MolecularActivityToChemicalEntityAssociation.__pydantic_model__.update_forward_refs()
MolecularActivityToMolecularActivityAssociation.__pydantic_model__.update_forward_refs()
GeneToGoTermAssociation.__pydantic_model__.update_forward_refs()
EntityToDiseaseAssociation.__pydantic_model__.update_forward_refs()
EntityToPhenotypicFeatureAssociation.__pydantic_model__.update_forward_refs()
SequenceAssociation.__pydantic_model__.update_forward_refs()
GenomicSequenceLocalization.__pydantic_model__.update_forward_refs()
SequenceFeatureRelationship.__pydantic_model__.update_forward_refs()
TranscriptToGeneRelationship.__pydantic_model__.update_forward_refs()
GeneToGeneProductRelationship.__pydantic_model__.update_forward_refs()
ExonToTranscriptRelationship.__pydantic_model__.update_forward_refs()
GeneRegulatoryRelationship.__pydantic_model__.update_forward_refs()
AnatomicalEntityToAnatomicalEntityAssociation.__pydantic_model__.update_forward_refs()
AnatomicalEntityToAnatomicalEntityPartOfAssociation.__pydantic_model__.update_forward_refs()
AnatomicalEntityToAnatomicalEntityOntogenicAssociation.__pydantic_model__.update_forward_refs()
OrganismTaxonToEntityAssociation.__pydantic_model__.update_forward_refs()
OrganismTaxonToOrganismTaxonAssociation.__pydantic_model__.update_forward_refs()
OrganismTaxonToOrganismTaxonSpecialization.__pydantic_model__.update_forward_refs()
OrganismTaxonToOrganismTaxonInteraction.__pydantic_model__.update_forward_refs()
OrganismTaxonToEnvironmentAssociation.__pydantic_model__.update_forward_refs()
