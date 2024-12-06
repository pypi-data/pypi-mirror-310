import numpy as np
import scipy.stats as stats
import math
import mne
from typing import List, Tuple, Union

from ctxgen.c import calc_membrane_potential


class CtxGen:
    """Context Generator (CTX-GEN).
    Generate a synthetic signal based on user-defined context states using
    multiple integrate-and-fire (LIF) models.

    Args:
        n_neurons (int, optional): Number of neurons. Defaults to 500.
        sfreq (int, optional): Sampling frequency for output. Defaults to 256.
        sfreq_gen (int, optional): Sampling frequency for
            calculating membrane potentials. Defaults to 2048.
        v_thresh (int, optional): Threshold potential. Defaults to 24.
        tau (float, optional): Time constant. Defaults to 0.02.
        verbose (bool, optional): Defaults to True.
    """

    def __init__(
        self,
        n_neurons: int = 500,
        sfreq: int = 256,
        sfreq_gen: int = 2048,
        v_thresh: int = 24,
        tau: float = 0.02,
        verbose: bool = True
    ) -> None:
        self.M = n_neurons
        self.v_thresh = v_thresh
        self.tau = tau
        self.sfreq = sfreq
        if not sfreq_gen:
            sfreq_gen = sfreq
        assert sfreq_gen >= sfreq, "[ctxgen] sfreq_gen must be >= sfreq"
        assert (sfreq_gen / sfreq) % 1 == 0., \
            "[ctxgen] sfreq_gen must be an int multiple of sfreq"
        self.delta_t = 1 / sfreq_gen
        self.verbose = verbose

        if verbose:
            print("[ctxgen] number of neurons:", n_neurons)
            print("[ctxgen] output sample frequency (Hz)", self.sfreq)
            print("[ctxgen] generation sample frequency (Hz):", sfreq_gen)
            print("[ctxgen] Δt:", self.delta_t)
        return

    def generate_signal(
        self,
        states: List[Tuple[int, int]],
        pad: int = 8,
        seed: int = 42,
        as_raw: bool = True,
    ) -> Union[Tuple[np.ndarray, np.ndarray], mne.io.Raw]:
        """Generate the signal by supplying context states.

        Args:
            states (List[Tuple[int, int]]): Context states as a list of
                tuple(firing rate, duration in secs).
            pad (int, optional): Padding in secs. Defaults to 8.
            seed (int, optional): Random seed. Defaults to 42.
            as_raw (bool, optional): Output as mne.io.Raw. Defaults to True.

        Returns:
            mne.io.Raw: if as_raw is True.
            Tuple[np.ndarray, np.ndarray]: as tuple of (signal, firing_rates)
                if as_raw is False.
        """
        # Convert context states to firing rates "fr"
        # we use a mask and keep track of indices to assembly later
        pad = int(pad / self.delta_t)
        fr, mask, state_idx = [], [], []
        N, i, j = 0, 0, 0
        for _fr, t in states:
            # Create a mask to indicate if padding is used
            _mask = np.repeat(True, repeats=int(t / self.delta_t))
            if pad > 0:
                pad_mask = np.repeat(False, repeats=pad)
                _mask = np.hstack([pad_mask, _mask, pad_mask])
            mask.append(_mask)
            n = _mask.shape[0]

            # Specify the firing rate for each time step
            fr.append(np.repeat(_fr, repeats=n))

            # Save indices of this state
            j = i + n
            state_idx.append((i, j))
            i = j

            # Increment total size
            N += n

            if self.verbose:
                print(f"[ctxgen] state:\t{_fr} Hz\tt={t}")

            continue

        fr = np.hstack(fr)
        mask = np.hstack(mask)
        assert fr.shape == (N,)
        assert mask.shape == (N,)

        # Calculate membrane potentials
        V = calc_membrane_potential(
            fr=fr,
            M=self.M,
            delta_t=self.delta_t,
            tau=self.tau,
            v_thresh=self.v_thresh,
            seed=seed
        )

        # Construct signal
        W = np.abs(stats.norm.rvs(
            loc=0,
            scale=1,
            size=self.M,
            random_state=seed
        ))
        x = np.dot(W, V)

        # Correct DC shift by removing the mean in each state
        # this is preferred over filtering low frequencies for reliability
        for i, j in state_idx:
            x[i : j] = x[i : j] - np.mean(x[i : j])
            continue

        # Remove padding
        x = x[mask]
        fr = fr[mask]
        N = np.sum(mask)
        assert x.shape == (N,)
        assert fr.shape == (N,)

        # Downsample to output frequency
        resample_step = int(1 / (self.sfreq * self.delta_t))
        N = math.ceil(N / resample_step)
        x = x[:: resample_step]
        fr = fr[:: resample_step]
        assert x.shape == (N,)
        assert fr.shape == (N,)

        if self.verbose:
            print(
                "[ctxgen] generated signal:"
                f" T={N / self.sfreq:.2f}s, N={N}, {self.sfreq} Hz"
            )

        if not as_raw:
            return x, fr

        # Convert to mne.io.Raw
        raw = mne.io.RawArray(
            data=np.vstack([x, fr]),
            info=mne.create_info(
                ch_names=["x", "fr"],
                ch_types=["misc", "misc"],
                sfreq=self.sfreq
            ),
            verbose=self.verbose
        )
        events = mne.find_events(
            raw=raw,
            stim_channel="fr",
            initial_event=True,
            consecutive=True,
            verbose=self.verbose
        )[1:]
        if len(events) > 0:
            raw.set_annotations(mne.annotations_from_events(
                events=events,
                sfreq=self.sfreq,
                event_desc={e[2] : "y" for e in events}
            ))

        return raw