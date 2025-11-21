# Quick push script for GrimMonitor (fish shell)
function gitquickpush
    set msg (string join ' ' $argv)
    if test -z "$msg"
        set msg "Quick update"
    end
    git add .
    git commit -m "$msg"
    git push
end
