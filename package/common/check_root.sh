if [[ $EUID -ne 0 ]]; then
    echo "Warning:Permissions need to be elevated, some package may need to be installed by root or sudo."
    return 1
fi
return 0