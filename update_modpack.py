from bs4 import BeautifulSoup
from urllib.request import urlopen
import zipfile
import tempfile
import os
from packaging import version


class UpdateModpack:

    def __init__(self, filepath, revision='', pack_format=0,
                 is_resource_pack=True):
        """
        Update a modpack to the latest rev of minecraft. This assumes
        that the only changes are the numerical version, and not base
        game behaviors or paths.
        Args:
            filepath: a string denoting the path to the zipfile to update, or
            a list of strings denoting the paths to multiple zipfiles.
            pack_format: if you already know the numerical value of the
            new pack format, use this instead of revision.
            revision: if you want to map to a specific version of minecraft,
            use this field for the minecraft revision.
            is_resource_pack (bool): True if editing resource packs, False
            if editing data packs.
        """
        self.is_resource_pack = is_resource_pack
        if pack_format == 0:
            self.pack_format = self.translate_revision(revision)
        else:
            self.pack_format = pack_format
        if isinstance(filepath, list):
            for path in filepath:
                self.update_modpack(path)
        else:
            self.update_modpack(filepath)

    def translate_revision(self, revision):
        return '18'  # until i can fix the revision behavior.

        revision_mapping = MinecraftRevisions(
            self.is_resource_pack).revision_mapping

        if revision == '':
            return list(revision_mapping.keys())[-1]
        for rev in revision_mapping:
            starting_rev, ending_rev = revision_mapping[rev]
            if version.parse(starting_rev) <= version.parse(revision) <= version.parse(ending_rev):
                return rev
        raise Exception(f'No valid revision translation found for {revision} '
                        f'in revisions {revision_mapping}')

    def update_modpack(self, filepath):
        if '.zip' not in filepath:
            zipfiles = [file for file in os.listdir(filepath) if '.zip' in file]
            if not zipfiles:
                raise Exception(f'Filepath {filepath} contains no zip files.')
            for file in zipfiles:
                self.update_zip(file)
        else:
            self.update_zip(filepath)

    def update_zip(self, zipname, filename='pack.mcmeta'):
        # generate a temp file
        print(f'updating file {zipname}')
        tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
        os.close(tmpfd)

        # create a temp copy of the archive with edited filename
        with zipfile.ZipFile(zipname, 'r') as zin:
            with zipfile.ZipFile(tmpname, 'w') as zout:
                zout.comment = zin.comment  # preserve the comment
                for item in zin.infolist():
                    if item.filename != filename:
                        zout.writestr(item, zin.read(item.filename))
                    else:
                        with zin.open(filename) as fp:
                            updated = self.update_mcmeta(fp.read().decode())
                            zout.writestr(item, updated)

        # replace with the temp archive
        os.remove(zipname)
        os.rename(tmpname, zipname)

    def update_mcmeta(self, outp):
        outp = eval(outp)
        outp['pack']['pack_format'] = self.pack_format
        return str(outp)


class MinecraftRevisions:
    # TODO: add this! there is no clean source of truth i can find on pack
    # format mapping to minecraft rev. I am going to just set this to default
    # to latest until I can figure out the right way to do this.

    url = 'https://minecraft.fandom.com/wiki/Pack_format'

    def __init__(self, is_resource_pack):
        self.is_resource_pack = is_resource_pack
        self.revision_mapping = self._get_current_revisions()

    @staticmethod
    def _convert_revision_to_integer_range(revision_range):

        def unify_format(revision):
            if revision.count('.') == 1:
                revision += '.0'
            return revision

        revision_range = revision_range.replace('-', '–')
        if '–' in revision_range:
            lower_rev, upper_rev = revision_range.split('–')
        else:
            lower_rev, upper_rev = revision_range, revision_range

        return unify_format(lower_rev), unify_format(upper_rev)

    def _get_current_revisions(self):
        """
        page = urlopen(self.url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        line_by_line = soup.get_text().replace('\n\n', '').split("\n")
        rev_dict = {}
        for line in line_by_line:
            print(line)
        if self.is_resource_pack:
            target_line = "Resource pack formats"
        else:
            target_line = "Data pack formats"
        start = line_by_line.index(target_line)
        if start <= 0:
            Exception('Failure in querying Minecraft Wiki. '
                      'No resource pack data detected.')
        start += 4 # to skip the value, versions, releases, breaking changes sections. see? i told you. spaghetti.
        for i in range(start, len(line_by_line)):
            rev_dict[line_by_line[i].strip()] = self._convert_revision_to_integer_range(line_by_line[i+2].strip())
            i += 4 # skip other values
        print(rev_dict)
        """
