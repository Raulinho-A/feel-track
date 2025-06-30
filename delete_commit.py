def callback(commit, metadata):
    # Elimina el commit con token filtrado
    return commit.original_id != b"6efc344de39c3de7777c6ef680619bc1f214f6ee"