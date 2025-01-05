document.addEventListener("DOMContentLoaded", () => {
    const grid = document.getElementById("sudoku-grid");

    // Create the Sudoku grid
    for (let i = 0; i < 81; i++) {
        const cell = document.createElement("input");
        cell.type = "text";
        cell.maxLength = 1; // Allow only one digit
        cell.oninput = (e) => {
            if (!/^[1-9]?$/.test(e.target.value)) {
                e.target.value = ""; // Allow only numbers 1-9
            }
        };
        grid.appendChild(cell);
    }

    const getBoardFromGrid = () => {
        const cells = document.querySelectorAll("#sudoku-grid input");
        const board = [];
        for (let i = 0; i < 81; i += 9) {
            board.push(
                Array.from(cells)
                    .slice(i, i + 9)
                    .map((cell) => (cell.value ? parseInt(cell.value) : 0))
            );
        }
        return board;
    };

    const setBoardToGrid = (board) => {
        const cells = document.querySelectorAll("#sudoku-grid input");
        cells.forEach((cell, i) => {
            const row = Math.floor(i / 9);
            const col = i % 9;
            cell.value = board[row][col] !== 0 ? board[row][col] : "";
        });
    };

    document.getElementById("solve").addEventListener("click", () => {
        const board = getBoardFromGrid();
        fetch("/solve", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ board }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    setBoardToGrid(data.board);
                } else {
                    alert(data.message || "An error occurred while solving.");
                }
            });
    });

    document.getElementById("clear").addEventListener("click", () => {
        document.querySelectorAll("#sudoku-grid input").forEach((cell) => {
            cell.value = "";
        });
    });

    document.getElementById("generate").addEventListener("click", () => {
        const difficulty = document.getElementById("difficulty").value;
        fetch("/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ difficulty }),
        })
            .then((response) => response.json())
            .then((data) => {
                setBoardToGrid(data.board);
            });
    });
});