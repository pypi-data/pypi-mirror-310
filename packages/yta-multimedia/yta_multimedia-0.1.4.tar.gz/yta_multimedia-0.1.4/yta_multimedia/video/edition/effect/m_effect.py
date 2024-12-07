from moviepy.Effect import Effect


class MEffect(Effect):
    """
    Effect to be applied on a single video without any
    other video dependence.
    """
    # TODO: Is this working (?)
    result_must_replace: bool = False
    """
    This parameter indicates if this effect, when applied,
    must replace the original clip part or, if False, must
    be concatenated.
    """