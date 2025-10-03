#!/bin/bash

SESSION="lice"
TRAIT="$HOME/work/traiter"

tmux new -s $SESSION -d
tmux rename-window -t $SESSION anoplura
tmux send-keys -t $SESSION "cd $TRAIT/AnopluraTraiter" C-m
tmux send-keys -t $SESSION "vv" C-m
tmux send-keys -t $SESSION "git status" C-m

tmux new-window -t $SESSION
tmux send-keys -t $SESSION "cd $TRAIT/AnopluraTraiter" C-m
tmux send-keys -t $SESSION "vv" C-m

tmux select-window -t $SESSION:1
tmux attach -t $SESSION
