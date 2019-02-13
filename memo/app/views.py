from django.shortcuts import render,redirect
from .models import Memo
from django.shortcuts import get_object_or_404
from .forms import MemoForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def index(request):
  memos = Memo.objects.all().order_by('-updated_datetime')
  return render(request, 'app/index.html', { 'memos': memos })


def detail(request, memo_id):
    #get_object_or_404 モデルの中のmemo_idにないidが
    #入力された時にエラーではなく404ページを表示する
  memo = get_object_or_404(Memo, id=memo_id)
  return render(request, 'app/detail.html', {'memo': memo})



#データベースに保存するときの典型的な形
def new_memo(request):
	if request.method == "POST":
		form = MemoForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('app:index')
	else:
		form = MemoForm
	return render(request, 'app/new_memo.html', {'form': form })



#method==GETのときは実行されない
@require_POST
def delete_memo(request, memo_id):
	memo = get_object_or_404(Memo, id=memo_id)
	memo.delete()
	return redirect('app:index')

#データベースの更新
def edit_memo(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id)
    if request.method == "POST":
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect('app:index')
    else:
        form = MemoForm(instance=memo)
    return render(request, 'app/edit_memo.html', {'form': form, 'memo':memo })
