import Bio
import pandas
import cobra
import coralme

import logging
log = logging.getLogger(__name__)

import collections

class ProcessData(object):
	"""Generic class for storing information about a process

	This class essentially acts as a database that contains all of the
	relevant information needed to construct a particular reaction. For
	example, to construct a transcription reaction, following information must
	be accessed in some way:

	 - nucleotide sequence of the transcription unit
	 - RNA_polymerase (w/ sigma factor)
	 - RNAs transcribed from transcription unit
	 - other processes involved in transcription of RNAs (splicing, etc.)

	ME-model reactions are built from information in these objects.

	Parameters
	----------
	id : str
		Identifier of the ProcessData instance.

	model : :class:`coralme.core.model.MEModel`
		ME-model that the ProcessData is associated with

	"""

	def __init__(self, id, model):
		self.id = id
		self._model = model
		# parents need to be updated every time the process is updated
		# a parent must have an update method
		self._parent_reactions = set()
		model.process_data.append(self)

	@property
	def model(self):
		"""
		Get the ME-model the process data is associated with

		Returns
		-------
		:class:`coralme.core.model.MEModel
			ME-model that uses this process data
		"""
		return self._model

	@property
	def parent_reactions(self):
		"""
		Get reactions that the ProcessData instance is used to construct.

		Returns
		-------
		set
			Parent reactions of ProcessData

		"""
		return {self._model.reactions.get_by_id(i) for i in self._parent_reactions}

	def update_parent_reactions(self):
		"""

		Executes the update() function for all reactions that the ProcessData
		instance is used to construct.

		"""
		reactions = self._model.reactions
		for i in self._parent_reactions:
			reactions.get_by_id(i).update()

	def __repr__(self):
		return '<{:s} {:s} at 0x{:x}>'.format(self.__class__.__name__, self.id, id(self))

class StoichiometricData(ProcessData):
	"""Encodes the stoichiometry for a metabolic reaction.

	StoichiometricData defines the metabolite stoichiometry and upper/lower
	bounds of metabolic reaction

	Parameters
	----------
	id : str
		Identifier of the metabolic reaction. Should be identical to the
		M-model reactions in most cases.

	model : :class:`coralme.core.model.MEModel`
		ME-model that the StoichiometricData is associated with

	Attributes
	----------
	_stoichiometry : dict
		Dictionary of {metabolite_id: stoichiometry} for reaction

	subreactions : :class:`collections.DefaultDict(int)`
		Cases where multiple enzymes (often carriers ie. Acyl Carrier Protein)
		are involved in a metabolic reactions.

	upper_bound : int
		Upper reaction bound of metabolic reaction. Should be identical to the
		M-model reactions in most cases.

	lower_bound : int
		Lower reaction bound of metabolic reaction. Should be identical to the
		M-model reactions in most cases.
	"""
	def __init__(self, id, model):
		ProcessData.__init__(self, id, model)
		self._stoichiometry = {}
		self.subreactions = collections.defaultdict(int)
		self.lower_bound = 0.
		self.upper_bound = 1000.

	@property
	def stoichiometry(self):
		"""
		Get or set metabolite stoichiometry for reaction.

		Returns
		-------
		dict
			Dictionary of {metabolite_id: stoichiometry}
		"""
		return self._stoichiometry

	@stoichiometry.setter
	def stoichiometry(self, value):
		if not isinstance(value, dict):
			raise TypeError('Stoichiometry must be a dict, not ({:s})'.format(type(value)))
		for k in value:
			if not isinstance(k, str):
				raise TypeError('Stoichiometry keys must be strings, not \'{:s}\'.'.format(type(k)))
		self._stoichiometry = value

class SubreactionData(ProcessData):
	"""
	Parameters
	----------
	id : str
		Identifier of the subreaction data. As a best practice, if the
		subreaction data details a modification, the ID should be prefixed
		with 'mod + _'

	model : :class:`coralme.core.model.MEModel`
		ME-model that the SubreactionData is associated with

	Attributes
	----------
	enzyme : list or str or None
		List of :attr:`coralme.core.component.Complex.id` s for enzymes that
		catalyze this process

		or

		String of single :attr:`coralme.core.component.Complex.id` for enzyme
		that catalyzes this process

	keff : float
		Effective turnover rate of enzyme(s) in subreaction process

	_element_contribution : dict
		If subreaction adds a chemical moiety to a macromolecules via a
		modification or other means, net element contribution of the
		modification process should be accounted for. This can be used to
		mass balance check each of the individual processes.

		Dictionary of {element: net_number_of_contributions}

	"""
	def __init__(self, id, model):
		ProcessData.__init__(self, id, model)
		self.stoichiometry = {}
		self.enzyme = None
		self.keff = 65.
		self._element_contribution = {}

	@property
	def element_contribution(self):
		"""
		Get net contribution of elements from subreaction process to
		macromolecule

		If subreaction adds a chemical moiety to a macromolecules via a
		modification or other means, net element contribution of the
		modification process should be accounted for. This can be used to
		mass balance check each of the individual processes.

		Returns
		-------
		dict
			Dictionary of {element: net_number_of_contributions}

		"""
		if self._element_contribution:
			return self._element_contribution
		else:
			contribution = { k:v for k,v in self.calculate_element_contribution().items() if v }

		# Return 'trivial' cases (only one modifying metabolite in the
		# reactants and no products) without warning
		if len(self.stoichiometry) == 1 and list(self.stoichiometry.values())[0] < 0:
			return self.calculate_element_contribution()
		elif contribution:
			logging.warning('No element contribution input for SubReaction \'{:s}\'. Calculating based on stoichiometry instead.'.format(self.id))
			return self.calculate_element_contribution()
		else:
			return {}

	@element_contribution.setter
	def element_contribution(self, value):
		if not isinstance(value, dict):
			raise TypeError('Elemental_contribution must be a dictionary, not \'{:s}\'.'.format(type(value)))
		self._element_contribution = value

	def calculate_element_contribution(self):
		"""
		Calculate net contribution of chemical elements based on the
		stoichiometry of the subreaction data

		Returns
		-------
		dict
			Dictionary of {element: net_number_of_contributions}

		"""
		elements = collections.defaultdict(int)
		for met, coefficient in self.stoichiometry.items():
			if self._model.metabolites.has_id(met):
				met_obj = self._model.metabolites.get_by_id(met)
			else:
				logging.warning('The metabolite \'{:s}\' must exist in the ME-model to calculate the element contribution.'.format(met))
				continue

			# elements lost in conversion are added to complex, protein, etc.
			if not met_obj.elements and not isinstance(met_obj, coralme.core.component.GenerictRNA):
				logging.warning('Metabolite \'{:s}\' does not have a formula. If it is a \'Complex\', its formula will be determined from amino acid composition and prosthetic groups. Otherwise, please set a formula in the M-model or in the metabolites.txt input file.'.format(met_obj.id))

			for e, n in met_obj.elements.items():
				elements[e] -= n * coefficient

		return elements

	def calculate_biomass_contribution(self):
		"""
		Calculate net biomass increase/decrease as a result of the subreaction
		process.

		If subreaction adds a chemical moiety to a macromolecules via a
		modification or other means, the biomass contribution of the
		modification process should be accounted for and ultimately included
		in the reaction it is involved in.

		Returns
		-------
		float
			Mass of moiety transferred to macromolecule by subreaction

		"""
		elements = self.element_contribution

		# Create temporary metabolite for calculating formula weight
		tmp_met = cobra.Metabolite('mass')
		coralme.util.massbalance.elements_to_formula(tmp_met, elements)

		return tmp_met.formula_weight

	def get_complex_data(self):
		"""
		Get the complex data that the subreaction is involved in

		Yields
		------
		:class:`coralme.core.processdata.ComplexData`
			ComplexData that subreaction is involved in
		"""
		for i in self._model.complex_data:
			if self.id in i.subreactions:
				yield i

	def get_all_usages(self):
		"""
		Get all process data that the subreaction is involved in

		Yields
		------
		:class:`coralme.core.processdata.ProcessData`
			ProcessData that subreaction is involved in
		"""
		for i in self._model.process_data:
			if hasattr(i, 'subreactions') and self.id in i.subreactions:
				yield i

class ComplexData(ProcessData):
	"""Contains all information associated with the formation of an
	functional enzyme complex.

	This can include any enzyme complex modifications required for the enzyme
	to become active.

	Parameters
	----------
	id : str
		Identifier of the complex data. As a best practice, this should
		typically use the same ID as the complex being formed. In cases with
		multiple ways to form complex '_ + alt' or similar suffixes can be
		used.

	model : :class:`coralme.core.model.MEModel`
		ME-model that the ComplexData is associated with

	Attributes
	----------

	stoichiometry : :class:`collections.DefaultDict(int)`
		Dictionary containing {protein_id: count} for all protein subunits
		comprising enzyme complex

	subreactions : dict
		Dictionary of {subreaction_data_id: count} for all complex formation
		subreactions/modifications. This can include cofactor/prosthetic group
		binding or enzyme side group addition.

	"""

	def __init__(self, id, model):
		ProcessData.__init__(self, id, model)
		# {Component.id: stoichiometry}
		self.stoichiometry = collections.defaultdict(float)
		# {SubreactionData.id : number}
		# Forming some metacomplexes occur in multiple steps
		self.subreactions = {}
		self._complex_id = None  # assumed to be the same as id if None

	@property
	def formation(self):
		"""Get the formation reaction object

		Returns
		-------
		:class:`coralme.core.reaction.ComplexFormation`
			Complex formation reaction detailed in ComplexData
		"""
		try:
			return self._model.reactions.get_by_id('formation_' + self.id)
		except KeyError:
			return None

	@property
	def complex(self):
		"""
		Get complex metabolite object

		Returns
		-------
		:class:`coralme.core.component.Complex`
			Instance of complex metabolite that ComplexData is used to
			synthesize
		"""
		return self._model.metabolites.get_by_id(self.complex_id)

	@property
	def complex_id(self):
		"""
		Get  and set complex ID for product of complex formation reaction

		There are cases where multiple equivalent processes can result in
		the same final complex. This allows the equivalent final complex
		complex_id to be queried. This only needs set in the above case

		Returns
		-------
		str
			ID of complex that ComplexData is used to synthesize
		"""

		return self.id if self._complex_id is None else self._complex_id

	@complex_id.setter
	def complex_id(self, value):
		self._complex_id = None if value == self.id else value

	def create_complex_formation(self, verbose=True):
		"""creates a complex formation reaction

		This assumes none exists already. Will create a reaction (prefixed by
		'formation') which forms the complex

		Parameters
		----------
		verbose : bool
			If True, print if a metabolite is added to model during update

		"""
		formation_id = 'formation_' + self.id
		if formation_id in self._model.reactions:
			raise ValueError('Reaction \'{:s}\' already in the ME-model.'.format(formation_id))
		formation = coralme.core.reaction.ComplexFormation(formation_id)
		formation.complex_data_id = self.id
		formation._complex_id = self.complex_id
		self._model.add_reactions([formation])
		formation.update(verbose = verbose)

class TranscriptionData(ProcessData):
	"""
	Class for storing information needed to define a transcription reaction

	Parameters
	----------
	id : str
		Identifier of the transcription unit, typically beginning with 'TU'

	model : :class:`coralme.core.model.MEModel`
		ME-model that the TranscriptionData is associated with

	Attributes
	----------

	nucleotide_sequence : str
		String of base pair abbreviations for nucleotides contained in the
		transcription unit

	RNA_products : set
		IDs of :class:`coralme.core.component.TranscribedGene` that the
		transcription unit encodes. Each member should be prefixed with
		'RNA + _'

	RNA_polymerase : str
		ID of the :class:`coralme.core.component.RNAP` that transcribes the
		transcription unit. Different IDs are used for different sigma factors

	subreactions : :class:`collections.DefaultDict(int)`
		Dictionary of
		{:class:`coralme.core.processdata.SubreactionData` ID: num_usages}
		required for the transcription unit to be transcribed

	"""
	def __init__(self, id, model, rna_products = set()):
		ProcessData.__init__(self, id, model)
		self.nucleotide_sequence = ''
		self.RNA_products = rna_products
		self.original_RNA_products = rna_products
		self.RNA_polymerase = ''
		# {SubreactionData.id : number}
		self._subreactions = collections.defaultdict(int)

	@property
	def n_cuts(self):
		# Number of cuts depends on the type of the RNAs in the TU
		return len([ x for x in self.RNA_types if x in ['rRNA', 'tRNA']]) * 2

	@property
	def n_excised(self):
		# Number of excised bases depends on the type of the RNAs in the TU
		if set(self.RNA_types) == {'mRNA'}:
			return 0
		else:
			return sum(self.excised_bases.values())

	@property
	def n_overlapping(self):
		if self.id == 'RNA_dummy' or len(self.RNA_products) == 0:
			return 0

		import pyranges

		ranges = []
		for rna in self.RNA_products:
			data = self.model.metabolites.get_by_id(rna)
			left_pos = data.left_pos[0].replace('>', '').replace('<', '')
			right_pos = data.right_pos[0].replace('>', '').replace('<', '')
			ranges.append(['X', left_pos, right_pos, data.strand])

		df = pandas.DataFrame(ranges, columns = ['Chromosome', 'Start', 'End', 'Strand'])
		ranges = pyranges.PyRanges(df)

		# add overlapping ranges to df
		res = ranges.intersect(ranges, strandedness = 'same').df

		# remove original ranges
		# WARNING: What does happen if a gene overlaps completely another?
		tmp = pandas.merge(res, ranges.df, how = 'outer', indicator = True)
		tmp = tmp[tmp['_merge'] == 'left_only'].drop_duplicates()

		# return total length of the overlaps
		return abs(tmp['Start'] - tmp['End']).sum().sum()

	@property
	def subreactions(self):
		data = self._subreactions

		# Number of cuts and excised bases depend on the type of the RNAs in the TU
		if 'rRNA' not in set(self.RNA_types) and 'tRNA' not in set(self.RNA_types):
			return data

		n_overlapping = self.n_overlapping
		n_excised = self.n_excised
		n_cuts = self.n_cuts

		# WARNING: Because first 'if', n_cuts cannot be zero
		#if n_excised == 0 or (n_excised + n_overlapping) == 0 or n_cuts == 0:
			#return data
		#if n_excised == 0:
			#n_cuts = 0

		rna_types = list(self.RNA_types)
		n_trna = rna_types.count('tRNA')

		if 'rRNA' in set(rna_types):
			data['rRNA_containing_excision'] = n_cuts
		elif n_trna == 1:
			data['monocistronic_excision'] = n_cuts
		elif n_trna > 1:
			data['polycistronic_wout_rRNA_excision'] = n_cuts
		else: # only applies to rnpB (RNase P catalytic RNA component)
			data['monocistronic_excision'] = n_cuts

		# The non functional RNA segments need degraded back to nucleotides
		# TODO check if RNA_degradation requirement is per nucleotide
		data['RNA_degradation_machine'] = n_cuts
		data['RNA_degradation_atp_requirement'] = n_excised + n_overlapping

		return { k:v for k,v in data.items() if v != 0 }

	@property
	def nucleotide_count(self):
		"""
		Get count of each nucleotide contained in the nucleotide sequence

		Returns
		-------
		dict
			{nuclotide_id: number_of_occurances}

		"""
		#return { coralme.util.dogma.transcription_table[i]: self.nucleotide_sequence.count(i) for i in ['A', 'T', 'G', 'C'] }
		#return { coralme.util.dogma.transcription_table[k]:v for k,v in collections.Counter(self.nucleotide_sequence).items() }
		if self.organelle is None:
			if self._model.global_info['domain'].lower() in ['prokaryote', 'bacteria']:
				return { coralme.util.dogma.transcription_table['c'][k]:v for k,v in collections.Counter(self.nucleotide_sequence).items() }
			if self._model.global_info['domain'].lower() in ['eukarya', 'eukaryote']:
				return { coralme.util.dogma.transcription_table['n'][k]:v for k,v in collections.Counter(self.nucleotide_sequence).items() }
			#return { coralme.util.dogma.transcription_table['n'][k]:v for k,v in collections.Counter(self.nucleotide_sequence).items() }
		elif self.organelle.lower() in ['mitochondria', 'mitochondrion']:
			return { coralme.util.dogma.transcription_table['m'][k]:v for k,v in collections.Counter(self.nucleotide_sequence).items() }
		elif self.organelle.lower() in ['chloroplast', 'plastid']:
			return { coralme.util.dogma.transcription_table['h'][k]:v for k,v in collections.Counter(self.nucleotide_sequence).items() }
		else:
			logging.warning('The \'organelle\' property of the feature \'{:s}\' is not \'mitochondria\' or \'chloroplast\'.'.format(self.id))
			return { coralme.util.dogma.transcription_table['n'][k]:v for k,v in collections.Counter(self.nucleotide_sequence).items() }

	@property
	def RNA_types(self):
		"""
		Get generator consisting of the RNA type for each RNA product

		Yields
		------
		str
			(mRNA, tRNA, rRNA, ncRNA)
		"""
		for rna in self.RNA_products:
			rna_type = self._model.metabolites.get_by_id(rna).RNA_type
			if rna_type:
				yield rna_type

	@property
	def excised_bases(self):
		"""
		Get count of bases that are excised during transcription

		If a stable RNA (e.g. tRNA or rRNA) is coded for in the transcription
		unit, the transcript must be spliced in order for these to function.

		This determines whether the transcription unit requires splicing and,
		if so, returns the count of nucleotides within the transcription unit
		that are not accounted for in the RNA products, thus identifying the
		appropriate introns nucleotides.

		Returns
		-------
		dict
			{nucleotide_monophosphate_id: number_excised}

			i.e. {'amp_c': 10, 'gmp_c': 11, 'ump_c': 9, 'cmp_c': 11}

		"""
		rna_types = set(self.RNA_types)

		# Skip if TU does not have any annotated RNA Products
		if len(rna_types) == 0:
			return {'amp_c': 0, 'gmp_c': 0, 'ump_c': 0, 'cmp_c': 0}

		# Skip if TU only codes for mRNA
		# WARNING: The GenBank can contain other types of RNAs that break the condition of only mRNAs in the TU
		if rna_types == {'mRNA'}:
			return {'amp_c': 0, 'gmp_c': 0, 'ump_c': 0, 'cmp_c': 0}

		# WARNING: Features in the TU can overlap, thus this calculation must be corrected
		# Get dictionary of all nucleotide counts for TU
		seq = self.nucleotide_sequence
		#counts = { i: seq.count(i) for i in ('A', 'T', 'G', 'C') }
		counts = collections.Counter(seq)

		# Subtract bases contained in RNA_product from dictionary
		metabolites = self._model.metabolites
		for product_id in self.RNA_products:
			gene_seq = metabolites.get_by_id(product_id).nucleotide_sequence
			#for b in ('A', 'T', 'G', 'C'):
				#counts[b] -= gene_seq.count(b)
			counts.subtract(collections.Counter(gene_seq)) # inplace

		# First base being a triphosphate will be handled by the reaction
		# producing an extra ppi during transcription. But generally, we add
		# triphosphate bases when transcribing, but excise monophosphate bases.
		#monophosphate_counts = { coralme.util.dogma.transcription_table[k].replace('tp_c', 'mp_c'):v for k,v in counts.items() }
		monophosphate_counts = { coralme.util.dogma.transcription_table['c'][k].replace('tp_c', 'mp_c'):v for k,v in counts.items() }
		return monophosphate_counts

	@property
	def codes_stable_rna(self):
		"""
		Get whether transcription unit codes for a stable RNA

		Returns
		-------
		bool
			True if tRNA or rRNA in RNA products
			False if not

		"""
		has_stable_rna = False
		for RNA in self.RNA_products:
			try:
				gene = self._model.metabolites.get_by_id(RNA)
			except KeyError:
				pass
			else:
				if gene.RNA_type in ['tRNA', 'rRNA', 'ncRNA']:
					has_stable_rna = True
		return has_stable_rna

class GenericData(ProcessData):
	"""
	Class for storing information about generic metabolites

	Parameters
	----------
	id : str
		Identifier of the generic metabolite. As a best practice, this ID
		should be prefixed with 'generic + _'

	model : :class:`coralme.core.model.MEModel`
		ME-model that the GenericData is associated with

	component_list : list
		List of metabolite ids for all metabolites that can provide
		identical functionality
	"""
	def __init__(self, id, model, component_list):
		if not id.startswith('generic_'):
			logging.warning('Best practice for generic id to start with the \'generic_\' prefix.')
		ProcessData.__init__(self, id, model)
		self.component_list = component_list

		# bypass problems with GenericData not having complex and complex_id attributes
		self._complex_id = None  # assumed to be the same as id if None

	# bypass problems with GenericData not having complex and complex_id attributes
	@property
	def complex(self):
		"""
		Get complex metabolite object

		Returns
		-------
		:class:`coralme.core.component.Complex`
			Instance of complex metabolite that ComplexData is used to
			synthesize
		"""
		return self._model.metabolites.get_by_id(self.complex_id)

	@property
	def complex_id(self):
		"""
		Get  and set complex ID for product of complex formation reaction

		There are cases where multiple equivalent processes can result in
		the same final complex. This allows the equivalent final complex
		complex_id to be queried. This only needs set in the above case

		Returns
		-------
		str
			ID of complex that ComplexData is used to synthesize
		"""

		return self.id if self._complex_id is None else self._complex_id

	@complex_id.setter
	def complex_id(self, value):
		self._complex_id = None if value == self.id else value

	def create_reactions(self):
		"""

		Adds reaction with id '<metabolite_id> + _ + to + _ + <generic_id>'
		for each metabolite in self.component_list.

		Creates generic metabolite and generic reaction, if they do not already
		exist.
		"""
		model = self._model
		try:
			generic_metabolite = model.metabolites.get_by_id(self.id)
		except KeyError:
			generic_metabolite = coralme.core.component.GenericComponent(self.id)
			model.add_metabolites([generic_metabolite])
		for c_id in [ x for x in self.component_list if x.replace('RNA_', '') not in model.global_info['knockouts'] ]:
			reaction_id = c_id + '_to_' + self.id
			try:
				reaction = model.reactions.get_by_id(reaction_id)
			except KeyError:
				reaction = coralme.core.reaction.GenericFormationReaction(reaction_id)
				model.add_reactions([reaction])
			stoic = {
				generic_metabolite: 1,
				model.metabolites.get_by_id(c_id): -1
				}
			reaction.add_metabolites(stoic, combine=False)

class TranslationData(ProcessData):
	"""
	Class for storing information about a translation reaction.

	Parameters
	----------
	id : str
		Identifier of the gene being translated, typically the locus tag

	model : :class:`coralme.core.model.MEModel`
		ME-model that the TranslationData is associated with

	mrna : str
		ID of the mRNA that is being translated

	protein : str
		ID of the protein product.

	Attributes
	----------
	mRNA : str
		ID of the mRNA that is being translated

	protein : str
		ID of the protein product.

	subreactions : :class:`collections.DefaultDict(int)`
		Dictionary of
		{:attr:`coralme.core.processdata.SubreactionData.id`: num_usages}
		required for the mRNA to be translated

	nucleotide_sequence : str
		String of base pair abbreviations for nucleotides contained in the gene
		being translated

	"""
	def __init__(self, id, model, mrna, protein):
		ProcessData.__init__(self, id, model)
		self.mRNA = mrna
		self.protein = protein
		self.subreactions = collections.defaultdict(int)
		self.nucleotide_sequence = ''

	@property
	def amino_acid_sequence(self):
		"""
		Get amino acid sequence from mRNA's nucleotide sequence

		Returns
		-------
		str
			Amino acid sequence

		"""
		#codons = (self.nucleotide_sequence[i: i + 3] for i in range(0, (len(self.nucleotide_sequence)), 3))
		#amino_acid_sequence = ''.join(coralme.util.dogma.codon_table[i] for i in codons)
		#amino_acid_sequence = str(Bio.Seq.Seq(self.nucleotide_sequence).translate(self._model.global_info['codon_table']))
		amino_acid_sequence = str(Bio.Seq.Seq(self.nucleotide_sequence).translate(self.transl_table))
		amino_acid_sequence = amino_acid_sequence.rstrip('*')
		if self.id != 'dummy':
			if amino_acid_sequence != self.translation:
				logging.warning('Protein sequence for \'{:s}\' from the GenBank file differs from the inferred from nucleotide sequence and translation table.'.format(self.id))
		if not amino_acid_sequence.startswith('M'):
			# alternate start codons translated as methionine
			amino_acid_sequence = 'M' + ''.join(amino_acid_sequence[1:])
		if '*' in amino_acid_sequence or 'U' in amino_acid_sequence: # translation of selenocysteine
			#amino_acid_sequence = amino_acid_sequence.replace('*', 'C') # Cysteine?
			amino_acid_sequence = amino_acid_sequence.replace('*', 'S') # Ser-tRNA is the precursor of Sec-tRNA
			amino_acid_sequence = amino_acid_sequence.replace('U', 'S') # Ser-tRNA is the precursor of Sec-tRNA

		return amino_acid_sequence

	@property
	def last_codon(self):
		"""
		Get the last codon contained in the mRNA sequence. This should
		correspond to the stop codon for the gene.

		Returns
		-------
		str
			Last 3 nucleotides comprising the last codon in the mRNA gene
			sequence

		"""
		return self.nucleotide_sequence[-3:].replace('T', 'U')

	@property
	def first_codon(self):
		"""
		Get the first codon contained in the mRNA sequence. This should
		correspond to the start codon for the gene.

		Returns
		-------
		str
			First 3 nucleotides comprising the first codon in the mRNA gene
			sequence

		"""
		return self.nucleotide_sequence[:+3].replace('T', 'U')

	def _itercodons(self):
		yield [i for i in self.codon_count]

	@property
	def codon_count(self):
		"""
		Get the number of each codon contained within the gene sequence

		Returns
		-------
		dict
			{codon_sequence: number_of_occurrences}

		"""
		#codons = (self.nucleotide_sequence[i: i+3] for i in range(0, len(self.nucleotide_sequence), 3))
		#codon_count = collections.defaultdict(int)
		#for i in codons:
			#codon_count[i.replace('T', 'U')] += 1

		codons = [self.nucleotide_sequence[i: i+3] for i in range(0, len(self.nucleotide_sequence), 3)]
		codons = [ x.replace('T', 'U') for x in codons if len(x) == 3 ]
		codon_count = collections.Counter(codons)

		return codon_count

	@property
	def amino_acid_count(self):
		"""Get number of each amino acid in the translated protein

		Returns
		-------
		dict
			{amino_acid_id: number_of_occurrences}
		"""

		#aa_count = collections.defaultdict(int)
		#for i in self.amino_acid_sequence:
			#aa_count[coralme.util.dogma.amino_acids[i]] += 1
		#return aa_count

		# Set compartment
		if self.organelle is None:
			compartment = '_c'
		elif self.organelle.lower() in ['mitochondria', 'mitochondrion']:
			compartment = '_m'
		elif self.organelle.lower() in ['chloroplast', 'plastid']:
			compartment = '_h'

		return { coralme.util.dogma.amino_acids[k] + compartment:v for k,v in collections.Counter(self.amino_acid_sequence).items() }

	@property
	def subreactions_from_sequence(self):
		"""
		Get subreactions associated with each tRNA/AA addition.

		tRNA activity is accounted for as subreactions. This returns the
		subreaction counts associated with each amino acid addition, based
		on the sequence of the mRNA.

		Returns
		-------
		dict
			{:attr:`coralme.core.processdata.SubreactionData.id`: num_usages}
		"""
		subreactions = {}

		#table = self._model.global_info['translation_table']
		# Trip first and last codon. Not translated during elongation
		codon_count = self.codon_count
		codon_count[self.first_codon] -= 1
		codon_count[self.last_codon] -= 1

		for codon, count in codon_count.items():
			if count == 0:
				continue

			codon = codon.replace('U', 'T')
			#if codon == 'TGA' and table == 11:
			if codon == 'TGA' and self.transl_table.id == 11:
				logging.warning('Adding selenocysteine for \'{:s}\', following translation table {:d} (See more https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi#SG{:d}).'.format(self.id, self.transl_table.id, self.transl_table.id))
				aa = 'sec'
			else:
				#abbreviated_aa = coralme.util.dogma.codon_table[codon]
				#abbreviated_aa = Bio.Seq.Seq(codon).translate(self._model.global_info['codon_table'])
				abbreviated_aa = Bio.Seq.Seq(codon).translate(self.transl_table)
				if abbreviated_aa == '*':
					break
				# Filter out the compartment and stereochemistry from aa id
				aa = coralme.util.dogma.amino_acids[abbreviated_aa].split('_')[0]
			codon = codon.replace('T', 'U')
			subreaction_id = aa + '_addition_at_' + codon
			#try:
				#self._model.process_data.get_by_id(subreaction_id)
			#except KeyError:
				#logging.warning('The tRNA SubReaction \'{:s}\' is not in the ME-model.'.format(subreaction_id))
			if self._model.process_data.has_id(subreaction_id):
				subreactions[subreaction_id] = count
			else:
				logging.warning('The tRNA SubReaction \'{:s}\' is not in the ME-model.'.format(subreaction_id))

		return subreactions

	def add_elongation_subreactions(self, elongation_subreactions=set()):
		"""
		Add all subreactions involved in translation elongation.

		This includes:

		 - tRNA activity subreactions returned with
		   :meth:`subreactions_from_sequence` which is called within this
		   function.

		 - Elongation subreactions passed into this function. These will be
		   added with a value of len(amino_acid_sequence) - 1 as these are
		   involved in each amino acid addition

		Some additional enzymatic processes are required for each amino acid
		addition during translation elongation

		Parameters
		----------
		elongation_subreactions : set
			Subreactions that are required for each amino acid addition

		"""

		for subreaction_id in elongation_subreactions:
			try:
				self._model.process_data.get_by_id(subreaction_id)
			except KeyError:
				logging.warning('Elongation SubReaction \'{:s}\' is not in ME-model. However, it can be added later.'.format(subreaction_id))
			else:
				# No elongation subreactions needed for start codon
				self.subreactions[subreaction_id] = len(self.amino_acid_sequence) - 1.

		for subreaction_id, value in self.subreactions_from_sequence.items():
			self.subreactions[subreaction_id] = value

	def add_initiation_subreactions(self, start_codons=set(), start_subreactions=set()):
		"""
		Add all subreactions involved in translation initiation.

		Parameters
		----------
		start_codons : set, optional
			Start codon sequences for the organism being modeled

		start_subreactions : set, optional
			Subreactions required to initiate translation, including the
			activity by the start tRNA

		"""
		#print(self.mRNA, type(self.mRNA), self.first_codon, type(self.first_codon))
		if self.first_codon not in start_codons:
			logging.warning('\'{:s}\' starts with \'{:s}\', which is not a start codon'.format(self.mRNA, str(self.first_codon)))

		for subreaction_id in start_subreactions:
			try:
				self._model.process_data.get_by_id(subreaction_id)
			except KeyError:
				logging.warning('Initiation SubReaction \'{:s}\' is not in the ME-model. However, it can be added later.'.format(subreaction_id))
			else:
				self.subreactions[subreaction_id] = 1

	def add_termination_subreactions(self, translation_terminator_dict=None):

		"""
		Add all subreactions involved in translation termination.

		Parameters
		----------
		translation_terminator_dict : dict or None
			{stop_codon : enzyme_id_of_terminator_enzyme}

		"""
		if not translation_terminator_dict:
			translation_terminator_dict = {}
		last_codon = self.last_codon
		term_enzyme = translation_terminator_dict.get(last_codon, None)
		if term_enzyme:
			termination_subreaction_id = last_codon + '_' + term_enzyme + '_mediated_termination_c'
			try:
				self._model.process_data.get_by_id(termination_subreaction_id)
			except KeyError:
				logging.warning('Termination SubReaction \'{:s}\' is not in ME-model. However, it can be added later.'.format(termination_subreaction_id))
			else:
				self.subreactions[termination_subreaction_id] = 1
		else:
			logging.warning('No termination enzyme for \'{:s}\'.'.format(self.mRNA))

class tRNAData(ProcessData):
	"""
	Class for storing information about a tRNA charging reaction.

	Parameters
	----------
	id : str
		Identifier for tRNA charging process. As best practice, this should
		be follow 'tRNA + _ + <tRNA_locus> + _ + <codon>' template. If tRNA
		initiates translation, <codon> should be replaced with START.

	model : :class:`coralme.core.model.MEModel`
		ME-model that the tRNAData is associated with

	amino_acid : str
		Amino acid that the tRNA transfers to an peptide

	rna : str
		ID of the uncharged tRNA metabolite. As a best practice, this ID should
		be prefixed with 'RNA + _'

	Attributes
	----------
	subreactions : :class:`collections.DefaultDict(int)`
		Dictionary of
		{:attr:`coralme.core.processdata.SubreactionData.id`: num_usages}
		required for the tRNA to be charged

	synthetase : str
		ID of the tRNA synthetase required to charge the tRNA with an amino
		acid

	synthetase_keff : float
		Effective turnover rate of the tRNA synthetase

	"""

	def __init__(self, id, model, amino_acid, rna, codon):
		ProcessData.__init__(self, id, model)
		self.codon = codon
		self.amino_acid = amino_acid
		self.RNA = rna
		self.subreactions = collections.defaultdict(int)
		self.synthetase = None
		self.synthetase_keff = 65.
		self.organelle = None

class TranslocationData(ProcessData):
	"""
	Class for storing information about a protein translocation pathway

	Parameters
	----------
	id : str
		Identifier for translocation pathway.

	model : :class:`coralme.core.model.MEModel`
		ME-model that the TranslocationData is associated with

	Attributes
	----------
	keff : float
		Effective turnover rate of the enzymes in the translocation pathway

	enzyme_dict : dict
		Dictionary containing enzyme specific information about the way it is
		coupled to protein translocation

		{enzyme_id: {length_dependent: <True or False>,
		 fixed_keff: <True or False>}}

	length_dependent_energy : bool
		True if the ATP cost of translocation is dependent on the length of
		the protein

	stoichiometry : dict
		Stoichiometry of translocation pathway, typically ATP/GTP hydrolysis

	"""

	def __init__(self, id, model):
		ProcessData.__init__(self, id, model)
		self.keff = 65.
		self.enzyme_dict = {}
		self.length_dependent_energy = False
		self.stoichiometry = {}

class PostTranslationData(ProcessData):
	"""
	Parameters
	----------
	id : str
		Identifier for post translation process.

	model : :class:`coralme.core.model.MEModel`
		ME-model that the PostTranslationData is associated with

	processed_protein : str
		ID of protein following post translational process

	preprocessed_protein : str
		ID of protein before post translational process

	Attributes
	----------
	translocation : set
		Translocation pathways involved in post translation reaction.

		Set of {:attr:`coralme.core.processdata.TranslocationData.id`}

	translocation_multipliers : dict
		Some proteins require different coupling of translocation enzymes.

		Dictionary of
		{:attr:`coralme.core.processdata.TranslocationData.id`: float}

	surface_area : dict
		If protein is translated into the inner or outer membrane, the surface
		area the protein occupies can be accounted for as well.

		Dictionary of {SA_+<inner_membrane or outer_membrane>: float}

	subreactions : :class:`collections.DefaultDict(float)`
		If a protein is modified following translation, this is accounted for
		here

		Dictionary of {subreaction_id: float}

	biomass_type : str
		If the subreactions add biomass to the translated gene, the
		biomass type (:attr:`coralme.core.compontent.Constraint.id`) of the
		modification must be defined.

	folding_mechanism : str
		ID of folding mechanism for post translation reaction

	aggregation_propensity : float
		Aggregation propensity for the protein

	keq_folding : dict
		Temperature dependant keq for folding protein

		Dictionary of {str(temperature): value}

	k_folding : dict
		Temperature dependant rate constant (k) for folding protein

		Dictionary of {str(temperature): value}

	propensity_scaling : float
		Some small peptides are more likely to be folded by certain
		chaperones. This is accounted for using propensity_scaling.

	"""

	def __init__(self, id, model, processed_protein, preprocessed_protein):
		ProcessData.__init__(self, id, model)
		self.processed_protein_id = processed_protein
		self.unprocessed_protein_id = preprocessed_protein

		# For translocation post translation reactions
		self.translocation = set()
		self.translocation_multipliers = {}
		self.surface_area = {}

		# For post translation modifications
		self.subreactions = collections.defaultdict(float)
		self.biomass_type = ''

		# For protein folding reactions (FoldME)
		self.folding_mechanism = ''
		self.aggregation_propensity = 0.
		self.keq_folding = {}
		self.k_folding = {}
		self.propensity_scaling = 1.
