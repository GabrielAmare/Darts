from tools37 import Console, Chart

console = Console(
    chart=Chart(
        **Console.DEFAULT_CHART.config,
        DO=dict(fg="#4ba91f", bg="#000000"),
        UNDO=dict(fg="#a93c1f", bg="#000000"),
        REDO=dict(fg="#4ba91f", bg="#000000"),
    ),
    # default_end=False,
    show_debug=True
)
