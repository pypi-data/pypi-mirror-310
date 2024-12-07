from ...AssetBundle import AssetBundle
from ...datasets.MuscimaPP import MuscimaPP
from smashcima.exporting.DebugGlyphRenderer import DebugGlyphRenderer
from .MppPage import MppPage
from smashcima.scene.SmuflLabels import SmuflLabels
from smashcima.scene.SmashcimaLabels import SmashcimaLabels
from .get_symbols import \
    get_full_noteheads, \
    get_empty_noteheads, \
    get_normal_barlines, \
    get_whole_rests, \
    get_half_rests, \
    get_quarter_rests, \
    get_eighth_rests, \
    get_sixteenth_rests, \
    get_g_clefs, \
    get_f_clefs, \
    get_c_clefs, \
    get_stems, \
    get_beams, \
    get_beam_hooks, \
    get_ledger_lines, \
    get_flags, \
    get_duration_dots, \
    get_staccato_dots, \
    get_accidentals, \
    get_brackets_and_braces, \
    get_time_marks
from .SymbolRepository import SymbolRepository
from .MppGlyphMetadata import MppGlyphMetadata
from pathlib import Path
import pickle
from tqdm import tqdm
import shutil
import cv2
from typing import Optional


# Re-install asset bunle during development by running:
# .venv/bin/python3 -m smashcima.assets.glyphs.muscima_pp --debug

class MuscimaPPGlyphs(AssetBundle):
    def __post_init__(self) -> None:
        self._symbol_repository_cache: Optional[SymbolRepository] = None

        self.muscima_pp = self.dependency_resolver.resolve_bundle(MuscimaPP)

    @property
    def symbol_repository_path(self) -> Path:
        return self.bundle_directory / "symbol_repository.pkl"
    
    def install(self):
        """Extracts data from the MUSCIMA++ dataset and bundles it up
        in the symbol repository in a pickle file."""
        document_paths = list(
            self.muscima_pp.cropobjects_directory.glob("CVC-MUSCIMA_*-ideal.xml")
        )

        repository = SymbolRepository()

        # go through all the MUSCIMA++ XML files
        for document_path in tqdm(document_paths):
            page = MppPage.load(document_path)

            # and extract glyphs
            repository.add_glyphs(get_full_noteheads(page))
            repository.add_glyphs(get_empty_noteheads(page))
            repository.add_glyphs(get_normal_barlines(page))
            repository.add_glyphs(get_whole_rests(page))
            repository.add_glyphs(get_half_rests(page))
            repository.add_glyphs(get_quarter_rests(page))
            repository.add_glyphs(get_eighth_rests(page))
            repository.add_glyphs(get_sixteenth_rests(page))
            repository.add_glyphs(get_g_clefs(page))
            repository.add_glyphs(get_f_clefs(page))
            repository.add_glyphs(get_c_clefs(page))
            repository.add_glyphs(get_stems(page))
            repository.add_glyphs(get_beams(page))
            repository.add_glyphs(get_beam_hooks(page))
            repository.add_glyphs(get_ledger_lines(page))
            repository.add_glyphs(get_duration_dots(page))
            repository.add_glyphs(get_staccato_dots(page))
            repository.add_glyphs(get_accidentals(page))
            repository.add_glyphs(get_brackets_and_braces(page))
            repository.add_glyphs(get_time_marks(page))
            # (flags must come after stems)
            glyphs_8th_flag, glyphs_16th_flag = get_flags(page)
            repository.add_glyphs(glyphs_8th_flag)
            repository.add_glyphs(glyphs_16th_flag)

            # and construct line indexes
            repository.index_lines([
                SmuflLabels.stem.value,
                SmashcimaLabels.beam.value,
                SmashcimaLabels.beamHook.value,
                SmashcimaLabels.ledgerLine.value
            ])

            # TODO: and extract distributions

        # dump the repository into a pickle file
        with open(self.symbol_repository_path, "wb") as file:
            pickle.dump(repository, file)
            print("Writing...", self.symbol_repository_path)
    
    def load_symbol_repository(self) -> SymbolRepository:
        """Loads the symbol repository from its pickle file"""
        if self._symbol_repository_cache is None:
            with open(self.symbol_repository_path, "rb") as file:
                repository = pickle.load(file)
            assert isinstance(repository, SymbolRepository)
            self._symbol_repository_cache = repository
        
        return self._symbol_repository_cache
    
    def build_debug_folder(self):
        """Creates a debug folder in the bundle folder, where it dumps
        all the extracted glyphs for visual inspection."""
        repository = self.load_symbol_repository()
        
        debug_folder = self.bundle_directory / "debug"
        shutil.rmtree(debug_folder, ignore_errors=True)
        debug_folder.mkdir()

        # glyphs
        glyph_renderer = DebugGlyphRenderer()
        for label, glyphs in repository.glyphs_by_class.items():
            glyphs_folder = debug_folder / label.replace(":", "-")
            glyphs_folder.mkdir()

            print(label, "...")
            for glyph in tqdm(glyphs):
                meta = MppGlyphMetadata.of_glyph(glyph)
                cv2.imwrite(
                    str(glyphs_folder / (meta.mpp_crop_object_uid + ".png")),
                    glyph_renderer.render(glyph)
                )
