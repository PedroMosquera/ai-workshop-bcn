/* === STATUS BOARD: state lives in this browser's localStorage only === */
class StatusBoard {
    static TEAMS = 5;
    static CHECKPOINTS = 3;
    static STATES = ['todo', 'wip', 'done', 'help'];
    static LABELS = { todo: '-', wip: 'in progress', done: 'done', help: 'need help' };
    static KEY = 'ws-board-v2';

    constructor() {
        this.body = document.getElementById('boardBody');
        this.state = this.load();
        this.render();
        document.getElementById('boardReset').addEventListener('click', () => {
            this.state = this.blank();
            this.save();
            this.render();
        });
    }

    blank() {
        return {
            teams: Array.from({ length: StatusBoard.TEAMS }, (_, i) => `Team ${i + 1}`),
            cells: Array.from({ length: StatusBoard.TEAMS }, () => Array(StatusBoard.CHECKPOINTS).fill('todo')),
        };
    }

    load() {
        try {
            const s = JSON.parse(localStorage.getItem(StatusBoard.KEY));
            if (s && s.teams?.length === StatusBoard.TEAMS && s.cells?.length === StatusBoard.TEAMS) return s;
        } catch (_) {}
        return this.blank();
    }

    save() {
        try { localStorage.setItem(StatusBoard.KEY, JSON.stringify(this.state)); } catch (_) {}
    }

    render() {
        const icons = `
            <svg class="i-wip" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor"/></svg>
            <svg class="i-done" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5L20 7"/></svg>
            <svg class="i-help" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M12 4v10M12 19v.5"/></svg>`;
        this.body.innerHTML = '';
        this.state.teams.forEach((name, t) => {
            const tr = document.createElement('tr');
            const th = document.createElement('td');
            th.className = 'team';
            th.contentEditable = 'true';
            th.spellcheck = false;
            th.textContent = name;
            th.addEventListener('blur', () => { this.state.teams[t] = th.textContent.trim() || `Team ${t + 1}`; this.save(); });
            th.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); th.blur(); } });
            tr.appendChild(th);
            this.state.cells[t].forEach((s, c) => {
                const td = document.createElement('td');
                td.className = 'cell';
                const b = document.createElement('button');
                b.type = 'button';
                b.className = 'st';
                b.innerHTML = `${icons}<span></span>`;
                const paint = () => {
                    const v = this.state.cells[t][c];
                    b.dataset.s = v;
                    b.querySelector('span').textContent = StatusBoard.LABELS[v];
                    b.setAttribute('aria-label', `${this.state.teams[t]}, checkpoint ${c + 1}: ${StatusBoard.LABELS[v]}`);
                };
                b.addEventListener('click', () => {
                    const i = StatusBoard.STATES.indexOf(this.state.cells[t][c]);
                    this.state.cells[t][c] = StatusBoard.STATES[(i + 1) % StatusBoard.STATES.length];
                    this.save();
                    paint();
                });
                paint();
                td.appendChild(b);
                tr.appendChild(td);
            });
            this.body.appendChild(tr);
        });
    }
}

new StatusBoard();
