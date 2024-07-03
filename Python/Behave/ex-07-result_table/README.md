
Goal:	Use result tables to simplify comparison of an expected dataset.
The usage of result tables come in variations. It often depends what you want to compare. These variations in the test automation layer are:

ordered dataset comparison
unordered dataset comparison
ordered subset comparison (result table contains subset)
unordered subset comparison (result table contains subset)

Hint:

The FIT test framework provides similar concepts via Fixtures. An extension of FIT, the FitLibrary, provides even more advanced fixtures classes/tables.

Dataset	Unordered comparison	Ordered Comparison
Subset	fitlibrary.SubsetFixture, fit.RowFixture (with table args)	fitlibrary.ArrayFixture (variant)
Complete	fit.RowFixture, fitlibrary.SetFixture	fitlibrary.ArrayFixture
Besides other descriptions of these Fixtures, the Fixture Gallery project provides examples for these fixture in several languages.

Both, unordered dataset comparison and unordered subset comparison are used in this tutorial in two different scenarios.