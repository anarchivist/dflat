import unittest
import shutil
from os import mkdir
from os.path import isdir, isfile, islink, basename, realpath

import dflat

class DflatTests(unittest.TestCase):

    def setUp(self):
        if isdir('dflat-test'):
            shutil.rmtree('dflat-test')
        # create a dflat home, and set it up with some initial contents 
        mkdir('dflat-test')
        open('dflat-test/a', 'w').write('the')
        open('dflat-test/b', 'w').write('sun')
        mkdir('dflat-test/c')
        open('dflat-test/c/1', 'w').write('will')
        open('dflat-test/c/2', 'w').write('shine')
        open('dflat-test/d b', 'w').write('and')

    def tearDown(self):
        if isdir('dflat-test'):
            shutil.rmtree('dflat-test')

    def atest_init(self):
        dflat.init('dflat-test')
        self.assertTrue(isdir('dflat-test'))
        self.assertTrue(isfile('dflat-test/dflat-info.txt'))
        self.assertTrue(islink('dflat-test/current'))
        self.assertEqual(basename(realpath('dflat-test/current')), 'v001')
        self.assertTrue(isdir('dflat-test/log'))
        self.assertTrue(isdir('dflat-test/v001/full/admin'))
        self.assertTrue(isdir('dflat-test/v001/full/annotation'))
        self.assertTrue(isdir('dflat-test/v001/full/data'))
        self.assertTrue(isdir('dflat-test/v001/full/enrichment'))
        self.assertTrue(isfile('dflat-test/v001/full/manifest.txt'))
        self.assertTrue(isfile('dflat-test/v001/full/relationships.ttl'))
        self.assertTrue(isfile('dflat-test/v001/full/splash.txt'))
        self.assertTrue(isfile('dflat-test/v001/full/data/a'))
        self.assertTrue(isfile('dflat-test/v001/full/data/b'))
        self.assertTrue(isdir('dflat-test/v001/full/data/c'))
        self.assertTrue(isfile('dflat-test/v001/full/data/c/1'))
        self.assertTrue(isfile('dflat-test/v001/full/data/c/2'))
        self.assertTrue(isfile('dflat-test/v001/full/data/d b'))

        # check manifest, ordering can be different with different pythons
        manifest = {}
        for line in open('dflat-test/v001/full/manifest.txt'):
            cols = line.split()
            manifest[cols[0]] = cols[2]
        manifest_files = manifest.keys()
        self.assertEqual(len(manifest_files), 7)
        self.assertTrue('splash.txt' in manifest_files)
        self.assertTrue('relationships.ttl' in manifest_files)
        self.assertTrue('data/b' in manifest_files)
        self.assertTrue('data/a' in manifest_files)
        self.assertTrue('data/c/2' in manifest_files)
        self.assertTrue('data/c/1' in manifest_files)
        self.assertTrue('data/d%20b' in manifest_files)
        self.assertEqual(manifest['splash.txt'], 'd41d8cd98f00b204e9800998ecf8427e')
        self.assertEqual(manifest['relationships.ttl'], 'd41d8cd98f00b204e9800998ecf8427e')
        self.assertEqual(manifest['data/b'], 'ebd556e6dfc99dbed29675ce1c6c68e5')
        self.assertEqual(manifest['data/a'], '8fc42c6ddf9966db3b09e84365034357')
        self.assertEqual(manifest['data/c/2'], '67c2c13e9cc0c312973c90245537fd04')
        self.assertEqual(manifest['data/c/1'], '18218139eec55d83cf82679934e5cd75')
        self.assertEqual(manifest['data/d%20b'], 'be5d5d37542d75f93a87094459f76678')

    def atest_checkout(self):
        dflat.init('dflat-test')
        dflat.checkout('dflat-test')
        self.assertTrue(isdir('dflat-test'))
        self.assertTrue(isfile('dflat-test/dflat-info.txt'))
        self.assertTrue(islink('dflat-test/current'))
        self.assertEqual(basename(realpath('dflat-test/current')), 'v001')
        self.assertTrue(isdir('dflat-test/log'))
        self.assertTrue(isdir('dflat-test/v002/full/admin'))
        self.assertTrue(isdir('dflat-test/v002/full/annotation'))
        self.assertTrue(isdir('dflat-test/v002/full/data'))
        self.assertTrue(isdir('dflat-test/v002/full/enrichment'))
        self.assertTrue(isfile('dflat-test/v002/full/manifest.txt'))
        self.assertTrue(isfile('dflat-test/v002/full/relationships.ttl'))
        self.assertTrue(isfile('dflat-test/v002/full/splash.txt'))
        self.assertTrue(isfile('dflat-test/v002/full/data/a'))
        self.assertTrue(isfile('dflat-test/v002/full/data/b'))
        self.assertTrue(isdir('dflat-test/v002/full/data/c'))
        self.assertTrue(isfile('dflat-test/v002/full/data/c/1'))
        self.assertTrue(isfile('dflat-test/v002/full/data/c/2'))

    def test_commit(self):
        if isdir('docs-dflat'):
            shutil.rmtree('docs-dflat')
        shutil.copytree('docs', 'docs-dflat')
        dflat.init('docs-dflat')
        dflat.checkout('docs-dflat')
        self.assertEqual(dflat._current_version('docs-dflat'), 'v001')
        f = open('docs-dflat/v002/full/data/reddspec.html', 'a')
        f.write('modification')
        f.close()
        dflat.commit('docs-dflat')
        self.assertEqual(dflat._current_version('docs-dflat'), 'v002')
        shutil.rmtree('docs-dflat')

    def atest_status(self):
        dflat.init('dflat-test')
        dflat.checkout('dflat-test')
        open('dflat-test/v002/full/data/d', 'w').write('foo')
        status = dflat.status('dflat-test')
        self.assertTrue('data/d' in status['added'])
