import collatex
from collatex.core_functions import export_alignment_table_as_tei

from acdh_collatex_utils.acdh_collatex_utils import chunks_to_df
from acdh_collatex_utils.collatex_patch import visualize_table_vertically_with_colors

from archiv.models import FrdCollationSample


def frd_collate(col_obj):
    df = chunks_to_df(col_obj.files())
    counter = 0
    for gr in df.groupby('chunk_nr'):
        counter += 1
        col_sample_id = f"{col_obj.hashes()}__{counter:03}"
        collation = collatex.Collation()
        cur_df = gr[1]
        for i, row in cur_df.iterrows():
            print(row['id'])
            collation.add_plain_witness(row['id'], row['text'])
        table = collatex.collate(collation)
        col_sample, _ = FrdCollationSample.objects.get_or_create(
            title_slug=col_sample_id,
            parent_col=col_obj
        )
        data = visualize_table_vertically_with_colors(
            table,
            collation
        )
        data_tei = export_alignment_table_as_tei(
            table,
            collation
        )
        col_sample.data_html = data
        col_sample.data_tei = data_tei
        col_sample.save()

    return col_obj
