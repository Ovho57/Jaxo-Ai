"""Optional terminal voice input/output for JAXO."""
class VoiceEngine:
    def __init__(self, console):
        self.console = console
        self.enabled = False
        self.engine = None

    def toggle(self):
        if self.enabled:
            self.enabled = False
            self.console.print("[dim]Voice replies disabled.[/dim]")
            return
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.enabled = True
            self.console.print("[green]Voice replies enabled.[/green]")
        except Exception as exc:
            self.console.print(f"[red]Could not start text-to-speech:[/] {exc}")
            self.console.print("[dim]Install optional packages from requirements-voice.txt.[/dim]")

    def speak(self, text):
        if not self.enabled or not self.engine:
            return
        try:
            import re
            clean = re.sub(r"[#>*_\x60]", " ", text)
            clean = re.sub(r"https?://\\S+", " link ", clean)
            self.engine.say(clean[:4000])
            self.engine.runAndWait()
        except Exception as exc:
            self.console.print(f"[yellow]Voice playback failed:[/] {exc}")

    def listen(self):
        try:
            import speech_recognition as sr
        except ImportError:
            self.console.print("[yellow]Voice input is optional. Install packages from requirements-voice.txt.[/yellow]")
            return None
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                self.console.print("[cyan]Listening... speak now.[/cyan]")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=20)
            self.console.print("[dim]Transcribing audio...[/dim]")
            return recognizer.recognize_google(audio)
        except sr.WaitTimeoutError:
            self.console.print("[yellow]No speech detected.[/yellow]")
        except sr.UnknownValueError:
            self.console.print("[yellow]I couldn't understand that audio.[/yellow]")
        except sr.RequestError as exc:
            self.console.print(f"[red]Speech recognition service error:[/] {exc}")
        except Exception as exc:
            self.console.print(f"[red]Microphone error:[/] {exc}")
            self.console.print("[dim]Check microphone permissions and install PyAudio.[/dim]")
        return None
