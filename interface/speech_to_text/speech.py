import torch
import string
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


punctuation_keep = "".join([char for char in string.punctuation if char not in ["'", '"', "-"]])
translator = str.maketrans('', '', punctuation_keep)

class SpeechToText:
    """
    A class to handle speech-to-text conversion using a pre-trained model.

    Attributes:
    device (str): The device to run the model on (CPU or GPU).
    torch_dtype (torch.dtype): The data type for the model (float16 for GPU, float32 for CPU).
    model_id (str): The identifier for the pre-trained model.
    model (AutoModelForSpeechSeq2Seq): The speech-to-text model pretrained.
    processor (AutoProcessor): The processor for the model.
    pipe (pipeline): The pipeline for automatic speech recognition.
    """

    def __init__(self):
        """
        Initialize the SpeechToText class with the appropriate model and processor.
        """
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        self.model_id = "openai/whisper-large-v3"
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_id, torch_dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
        )
        self.model.to(self.device)
        self.processor = AutoProcessor.from_pretrained(self.model_id)

        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=30,
            batch_size=64,
            return_timestamps=True,
            torch_dtype=self.torch_dtype,
            device=self.device,
        )

    def transcribe(self, audio_output):
        """
        Transcribe audio output to text.

        Parameters:
        audio_output (str): The audio output to be transcribed.

        Returns:
        str: The transcribed text.
        """
        results = self.pipe(audio_output)
        results = results['text'].lower()
        results = results.translate(translator)
        return results