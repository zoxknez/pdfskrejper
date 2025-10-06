"""
Interaktivni korisnički interfejs za PDF scraper.
"""

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from typing import Optional, Dict, List

from config.sources import SourceType, get_sources_by_type, Source

console = Console()


class InteractiveMenu:
    """Interaktivni meni za odabir opcija."""
    
    def __init__(self):
        self.selected_category: Optional[SourceType] = None
        self.selected_source: Optional[Source] = None
        self.search_query: str = ""
        self.max_results: int = 50
        self.custom_url: str = ""
    
    def show_welcome(self):
        """Prikazuje welcome poruku."""
        console.clear()
        console.print()
        console.print(Panel.fit(
            "[bold cyan]📄 PDF SCRAPER APLIKACIJA[/bold cyan]\n\n"
            "[dim]Automatsko preuzimanje PDF dokumenata sa interneta[/dim]",
            border_style="cyan"
        ))
        console.print()
    
    def select_category(self) -> SourceType:
        """Omogućava korisniku da izabere kategoriju."""
        console.print("[bold]Izaberite kategoriju dokumenata:[/bold]\n")
        
        categories = [
            ("1", SourceType.BOOKS, "📚 Knjige", "Besplatne knjige i e-books"),
            ("2", SourceType.RESEARCH, "🔬 Naučni radovi", "Research papers i studije"),
            ("3", SourceType.MAGAZINES, "📰 Časopisi", "Magazini i periodika"),
            ("4", SourceType.DOCUMENTS, "📄 Dokumenti", "Ostali dokumenti"),
        ]
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Broj", style="dim", width=6)
        table.add_column("Kategorija", style="cyan")
        table.add_column("Opis", style="dim")
        
        for num, cat_type, name, desc in categories:
            table.add_row(num, name, desc)
        
        console.print(table)
        console.print()
        
        choice = Prompt.ask(
            "Vaš izbor",
            choices=["1", "2", "3", "4"],
            default="1"
        )
        
        category_map = {
            "1": SourceType.BOOKS,
            "2": SourceType.RESEARCH,
            "3": SourceType.MAGAZINES,
            "4": SourceType.DOCUMENTS,
        }
        
        self.selected_category = category_map[choice]
        return self.selected_category
    
    def select_source(self) -> Source:
        """Omogućava korisniku da izabere izvor."""
        sources = get_sources_by_type(self.selected_category)
        
        if not sources:
            console.print("[yellow]Nema dostupnih izvora za ovu kategoriju.[/yellow]")
            return None
        
        console.print(f"\n[bold]Izaberite izvor za {self.selected_category.value}:[/bold]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Broj", style="dim", width=6)
        table.add_column("Izvor", style="cyan")
        table.add_column("Opis", style="dim")
        
        for idx, source in enumerate(sources, 1):
            table.add_row(
                str(idx),
                source.name,
                source.description
            )
        
        console.print(table)
        console.print()
        
        if len(sources) == 1:
            choice = "1"
            console.print(f"[dim]Automatski izabran: {sources[0].name}[/dim]\n")
        else:
            choice = Prompt.ask(
                "Vaš izbor",
                choices=[str(i) for i in range(1, len(sources) + 1)],
                default="1"
            )
        
        self.selected_source = sources[int(choice) - 1]
        return self.selected_source
    
    def get_search_query(self) -> str:
        """Traži search query od korisnika."""
        console.print()
        
        use_search = Confirm.ask(
            "Da li želite da pretražujete specifične termine?",
            default=True
        )
        
        if use_search:
            self.search_query = Prompt.ask(
                "Unesite pretragu (keywords)",
                default=""
            )
        else:
            self.search_query = ""
        
        return self.search_query
    
    def get_max_results(self) -> int:
        """Traži maksimalan broj rezultata."""
        console.print()
        
        max_input = Prompt.ask(
            "Maksimalan broj rezultata",
            default="50"
        )
        
        try:
            self.max_results = int(max_input)
        except ValueError:
            console.print("[yellow]Nevažeći broj, koristim 50[/yellow]")
            self.max_results = 50
        
        return self.max_results
    
    def get_custom_url(self) -> str:
        """Traži custom URL za scraping."""
        console.print()
        
        self.custom_url = Prompt.ask(
            "Unesite URL za scraping",
            default=""
        )
        
        return self.custom_url
    
    def confirm_settings(self) -> bool:
        """Prikazuje i potvrđuje izabrane postavke."""
        console.print()
        console.print("[bold]Pregled postavki:[/bold]\n")
        
        settings_table = Table(show_header=False, box=None)
        settings_table.add_column("Postavka", style="cyan")
        settings_table.add_column("Vrednost", style="green")
        
        settings_table.add_row("Kategorija:", self.selected_category.value if self.selected_category else "N/A")
        settings_table.add_row("Izvor:", self.selected_source.name if self.selected_source else "N/A")
        settings_table.add_row("Pretraga:", self.search_query or "(sve)")
        settings_table.add_row("Limit rezultata:", str(self.max_results))
        
        if self.custom_url:
            settings_table.add_row("Custom URL:", self.custom_url)
        
        console.print(settings_table)
        console.print()
        
        return Confirm.ask("Da li želite da nastavite?", default=True)
    
    def run(self) -> Dict:
        """Pokreće interaktivni meni i vraća konfiguraciju."""
        self.show_welcome()
        
        # Kategorija
        self.select_category()
        
        # Custom URL za DOCUMENTS kategoriju
        if self.selected_category == SourceType.DOCUMENTS:
            self.get_custom_url()
            if not self.custom_url:
                console.print("[red]Morate uneti URL za scraping![/red]")
                return None
        else:
            # Izvor
            self.select_source()
            if not self.selected_source:
                return None
        
        # Search query
        self.get_search_query()
        
        # Limit
        self.get_max_results()
        
        # Potvrda
        if not self.confirm_settings():
            console.print("[yellow]Otkazano.[/yellow]")
            return None
        
        # Vrati konfiguraciju
        return {
            'category': self.selected_category,
            'source': self.selected_source,
            'query': self.search_query,
            'max_results': self.max_results,
            'custom_url': self.custom_url,
        }
    
    @staticmethod
    def show_results(stats: Dict):
        """Prikazuje rezultate scraping-a."""
        console.print()
        console.print(Panel.fit(
            f"[bold green]✓ Scraping završen![/bold green]\n\n"
            f"Pronađeno URL-ova: [cyan]{stats.get('total_urls_found', 0)}[/cyan]\n"
            f"Uspešno preuzeto: [green]{stats.get('total_downloaded', 0)}[/green]\n"
            f"Neuspešno: [red]{stats.get('total_failed', 0)}[/red]\n"
            f"Uspešnost: [yellow]{stats.get('success_rate', 0):.1f}%[/yellow]",
            border_style="green"
        ))
        console.print()
