from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from cobalt import CobaltDataset, Workspace
from cobalt.embedding_models import SentenceTransformerEmbeddingModel
from cobalt.graph_utils import multi_level_graph_to_subsets_with_aggregation
from cobalt.lab.neighbors import generate_cluster_df_at_levels
from cobalt.text.ctfidf import top_keywords_per_level_per_subset


def describe_groups_multiresolution(
    ds: CobaltDataset,
    text_column_name: str,
    n_gram_range: Union[str, Tuple],
    min_level: int = 0,
    max_level: Optional[int] = None,
    max_keywords: int = 3,
    return_intermediates: bool = False,
) -> Tuple[pd.DataFrame, Workspace, Dict[int, Dict[int, str]]]:
    """Returns a summary of groups in a set of texts.

    This builds a multiresolution graph from the embeddings provided in the
    input dataset, and for a range of coarseness levels, computes a keyword
    description of the text contained in each node, and returns this information
    in a DataFrame.

    Optionally also returns a Workspace object that can be used to access the
    graph and explore the results further.

    Args:
        ds (CobaltDataset): Dataset (containing an embedding of the text data)
        text_column_name (str): Column containing text data for keyword analysis.
        n_gram_range (Union[str, Tuple]): Whether to analyze keywords with
            unigrams, bigrams, or a combination.
        min_level (int): Minumum graph level to output cluster labels for.
        max_level (int): Maximum graph level to output cluster labels for.
        max_keywords (int): Maximum number of keywords to find for each cluster.
        return_intermediates (bool): Whether to return intermediate results.

    Returns:
        A tuple consisting of a pd.DataFrame per level with the labels for each cluster,
        a Workspace object and the raw labels per level per node.


    """
    aggregation_columns = ds.df.select_dtypes(include=np.number).columns.tolist()

    w = Workspace(ds)
    g = w.new_graph()

    labels = top_keywords_per_level_per_subset(
        ds, g, text_column_name, n_keywords=max_keywords, n_gram_range=n_gram_range
    )

    if max_level is None:
        max_level = len(g.levels)

    summary_df = generate_cluster_df_at_levels(g, labels, (min_level, max_level))

    # Return Type: List[List]
    # Outer List is per level, Inner List is per subset.
    # Item is a pd.Series of different columns with their aggregated scores.
    aggregated_scores_by_level = multi_level_graph_to_subsets_with_aggregation(
        g, ds, aggregation_columns, min_level, max_level
    )

    # This is directly insertable into the `summary_df` _by construction_.
    d = {}
    for col in aggregation_columns:
        scores_stacked = []
        for aggregated_scores_per_subset in aggregated_scores_by_level:

            for score_set in aggregated_scores_per_subset:
                scores_stacked.append(score_set[col])
        d[col] = scores_stacked

    summary_df = pd.concat([summary_df, pd.DataFrame(d)], axis=1)

    no_neighbors = True

    if no_neighbors:
        cols = ["Label", "Node Size", "level", *aggregation_columns]
        summary_df = summary_df[cols]
        summary_df = summary_df.rename(columns={"Node Size": "query_count"})

    # The (w, labels) are useful for visualization.
    if return_intermediates:
        return summary_df, w, labels
    return summary_df


def raw_group_description_multiresolution(
    texts: List[str],
    numerical_data: Optional[Union[np.ndarray, pd.DataFrame]] = None,
    device: str = "mps",
    sentence_transformer_model_id: str = "all-MiniLM-L6-v2",
    min_level: int = 0,
    max_level: Optional[int] = None,
    max_keywords: int = 3,
    return_intermediates: bool = False,
) -> Tuple[pd.DataFrame, Workspace, Dict[int, Dict[int, str]]]:
    """Returns summary of groups in a set of texts, constructing a workspace along the way.

    Args:
        texts (List[str]): the texts to embed and analyze
        numerical_data : scoring column(s) as np.ndarray or dataframe.
        device (str): the device to run the embedding computation on
        sentence_transformer_model_id (str): SBERT ID
        min_level (int): Minumum Graph Level to output cluster labels for.
        max_level (int): Maximum Graph Level to output cluster labels for.
        max_keywords (int): Max Keywords to find in TFIDF algorithm.
        return_intermediates (bool): whether to return intermediate results or not.

    Returns:
        tuple (Tuple): consisting of a pd.DataFrame per level, the labels for each cluster.
            a workspace object and the raw labels per level per node.

    Notes:
        `numerical_data` really could be a dataframe but since all it needs to be right now
          is a np.ndarray,
        I implemented it as simply as possible. Lower-level, there is capability for it to
        use different aggregation methods. But that's not really necessary right now.

        The device is defaulted to be `mps` because that's what we're using internally and I didn't
        want to break the order of the API.

    """
    df = pd.DataFrame({"text": texts})

    if numerical_data is not None:
        if isinstance(numerical_data, pd.DataFrame):
            df = pd.concat([df, numerical_data], axis=1)
        else:
            df["score"] = numerical_data

    ds = CobaltDataset(df)
    m = SentenceTransformerEmbeddingModel(sentence_transformer_model_id)
    embedding = m.embed(texts, device=device)
    ds.add_embedding_array(embedding, metric="cosine", name="sbert")
    return describe_groups_multiresolution(
        ds, "text", "unigrams", min_level, max_level, max_keywords, return_intermediates
    )


def get_interpretable_groups(
    ds: CobaltDataset,
    text_column_name: str,
    n_gram_range: Union[str, Tuple],
    min_level: int = 0,
    max_level: Optional[int] = None,
    max_keywords: int = 3,
    return_intermediates: bool = False,
) -> Tuple[pd.DataFrame, Workspace, Dict[int, Dict[int, str]]]:
    """Returns summary of groups in a set of texts, constructing a workspace along the way.

    Args:
        ds (CobaltDataset): Dataset (with one embedding)
        text_column_name (str): COlumn containing text to construct keywords out of.
        n_gram_range (Union[str, Tuple]): Whether to do unigrams, bigrams, or a combination.
        min_level (int): Minumum Graph Level to output cluster labels for.
        max_level (int): Maximum Graph Level to output cluster labels for.
        max_keywords (int): Max Keywords to find in TFIDF algorithm.
        return_intermediates (bool): whether to return intermediate results or not.

    Returns:
        tuple (Tuple): consisting of a pd.DataFrame per level, the labels for each cluster.
            a workspace object and the raw labels per level per node.


    """
    # This function name is a compatibility shim to support external-facing notebook.
    return describe_groups_multiresolution(
        ds,
        text_column_name,
        n_gram_range,
        min_level,
        max_level,
        max_keywords,
        return_intermediates,
    )
